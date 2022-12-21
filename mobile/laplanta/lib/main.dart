import 'package:flutter/material.dart';
import 'package:laplanta/splash_screen.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import 'package:laplanta/services/api.dart';
import 'package:laplanta/widgets/my_plants.dart';

final apiProvider = Provider((ref) => Api());

void main() {
  runApp(const ProviderScope(child:LaplantaApp()));
}

alert(BuildContext context, String message) {
  Widget okButton = TextButton(
    child: const Text("OK"),
    onPressed: () => Navigator.of(context, rootNavigator: true).pop()
  );
  AlertDialog alert = AlertDialog(
    title: const Text("Error"),
    content: Text(message),
    actions: [
      okButton,
    ],
  );
  showDialog(
    context: context,
    builder: (BuildContext context) {
      return alert;
    },
  );
}

class LaplantaApp extends StatelessWidget {
  const LaplantaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "Laplanta",
      debugShowCheckedModeBanner: false,
      theme: ThemeData(primarySwatch: Colors.green),
      home: const SplashScreen(),
    );
  }
}
