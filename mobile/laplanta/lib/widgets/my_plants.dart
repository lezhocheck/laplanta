import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:laplanta/side_panel_header.dart';
import 'package:laplanta/widgets/app_bar.dart';
import 'package:laplanta/services/api.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:laplanta/main.dart';

class MyPlantsPage extends ConsumerStatefulWidget {
  const MyPlantsPage({super.key, required this.title});

  final String title;

  @override
  ConsumerState<MyPlantsPage> createState() => _MyPlantsPageState();
}

class FixedColumnWidget extends StatelessWidget {
  final Map<String, dynamic> data;

  const FixedColumnWidget({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    return DataTable(
        columnSpacing: 10,
        headingRowColor: MaterialStateProperty.all(Colors.green[300]),
        decoration: const BoxDecoration(
          border: Border(
            right: BorderSide(
              color: Colors.grey,
              width: 1,
            ),
          ),
        ),
        columns: const [
          DataColumn(label: Text('id')),
        ],
        rows: data["plants"]
            .map<DataRow>((item) => DataRow(cells: <DataCell>[
                  DataCell(Text(item["_id"].toString(),
                      style: const TextStyle(fontWeight: FontWeight.bold))),
                ]))
            .toList());
  }
}

class ScrollableColumnWidget extends StatelessWidget {

  final Map<String, dynamic> data;

  const ScrollableColumnWidget({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: DataTable(
            headingRowColor: MaterialStateProperty.all(Colors.green[100]),
            columnSpacing: 40,
            decoration: const BoxDecoration(
              border: Border(
                right: BorderSide(
                  color: Colors.grey,
                  width: 0.5,
                ),
              ),
            ),
            columns: const [
              DataColumn(label: Text('id')),
              DataColumn(label: Text('name')),
              DataColumn(label: Text('added_date')),
              DataColumn(label: Text('description')),
              DataColumn(label: Text('status'))
            ],
            rows: data["plants"]
            .map<DataRow>((item) => DataRow(cells: <DataCell>[
              DataCell(
                    Container(
                      alignment: AlignmentDirectional.center,
                      child: Text(
                        item["_id"].toString(),
                        style: const TextStyle(fontWeight: FontWeight.bold),
                ))),
                DataCell(
                    Container(
                      alignment: AlignmentDirectional.center,
                      child: Text(
                        item["name"].toString(),
                        style: const TextStyle(fontWeight: FontWeight.bold),
                ))),
                DataCell(
                    Container(
                      alignment: AlignmentDirectional.center,
                      child: Text(
                        item["added_date"].toString(),
                        style: const TextStyle(fontWeight: FontWeight.bold),
                ))),
                DataCell(
                    Container(
                      alignment: AlignmentDirectional.center,
                      child: Text(
                        item["description"].toString(),
                        style: const TextStyle(fontWeight: FontWeight.bold),
                ))),
                DataCell(
                    Container(
                      alignment: AlignmentDirectional.center,
                      child: Text(
                        item["status"].toString(),
                        style: const TextStyle(fontWeight: FontWeight.bold),
                ))),
                ]))
            .toList())
      ),
    );
  }
}

class _MyPlantsPageState extends ConsumerState<MyPlantsPage> {
  Map<String, dynamic> data = {
    "plants": [
      {
        "_id": "-",
        "added_date": "-",
        "description": "-",
        "image_path": "-",
        "name": "-",
        "status": "-"
      }
    ]
  };

  @override
  void initState() {
    super.initState();
    Api api = ref.read(apiProvider);
    WidgetsBinding.instance.addPostFrameCallback((_) async {
      try {
        var response = await api.dio.get('${Api.connection}/plants');
        if (!mounted) return;
        setState(() {
          data = jsonDecode(response.toString())["msg"];
        });
      } on DioError catch (error) {
        if (error.response != null) {
          var json = jsonDecode(error.response.toString());
          alert(context, json['msg'].toString());
        }
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: LaplantaAppBar(
        title: widget.title,
      ),
      body: SafeArea(
          child: SingleChildScrollView(
            child: Row(
              children: [
                //FixedColumnWidget(data: data),
                ScrollableColumnWidget(data: data),
              ],
            ),
          ),
    ));
  }
}
