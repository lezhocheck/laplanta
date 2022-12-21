import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class Api {
  Dio dio = Dio();
  String? accessToken;

  static const String connection = "http://localhost:9999";
  final _storage = const FlutterSecureStorage();

  Api() {
    dio.interceptors
        .add(InterceptorsWrapper(onRequest: (options, handler) async {
      if (!options.path.contains('http')) {
        options.path = connection + options.path;
      }
      options.headers['Authorization'] = 'Bearer $accessToken';
      return handler.next(options);
    }, onError: (DioError error, handler) async {
      if (error.response?.statusCode == 401) {
        if (await _storage.containsKey(key: 'refreshToken')) {
          await _refreshToken();
          return handler.resolve(await _retry(error.requestOptions));
        }
      }
      return handler.next(error);
    }));
  }

  Future<void> _refreshToken() async {
    final refreshToken = await _storage.read(key: 'refreshToken');
    final response =
        await dio.post('/refresh');
    if (response.statusCode == 200) {
      accessToken = response.data?.token;
    } else {
      accessToken = null;
      _storage.deleteAll();
    }
  }

  Future<Response<dynamic>> _retry(RequestOptions requestOptions) async {
    final options = Options(
      method: requestOptions.method,
      headers: requestOptions.headers,
    );
    return dio.request<dynamic>(requestOptions.path,
        data: requestOptions.data,
        queryParameters: requestOptions.queryParameters,
        options: options);
  }
}
