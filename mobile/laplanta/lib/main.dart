import 'package:flutter/material.dart';
import 'package:laplanta/splash_screen.dart';

void main() {
  runApp(const LaplantaApp());
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
