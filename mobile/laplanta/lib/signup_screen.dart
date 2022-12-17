import 'package:flutter/material.dart';
import 'package:laplanta/login_screen.dart';

class SignUpScreen extends StatefulWidget {
  const SignUpScreen({super.key});

  @override
  State<StatefulWidget> createState() => InitState();
}

class InitState extends State<SignUpScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: SingleChildScrollView(
            child: Column(
      children: [
        Container(
          height: 300,
          decoration: const BoxDecoration(
            borderRadius: BorderRadius.only(bottomLeft: Radius.circular(90)),
            color: Colors.green,
            gradient: LinearGradient(
              colors: [Colors.green, Colors.greenAccent],
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
            ),
          ),
          child: Center(
              child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Container(
                margin: const EdgeInsets.only(top: 50),
                child: const Icon(
                  Icons.spa,
                  size: 120,
                  color: Colors.white,
                ),
              ),
              Container(
                margin: const EdgeInsets.only(right: 20, top: 20),
                alignment: Alignment.bottomRight,
                child: const Text(
                  "Register",
                  style: TextStyle(fontSize: 40, color: Colors.white),
                ),
              )
            ],
          )),
        ),
        Container(
          alignment: Alignment.center,
          margin: const EdgeInsets.only(left: 20, right: 20, top: 70),
          padding: const EdgeInsets.only(left: 20, right: 20),
          height: 54,
          decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(50), color: Colors.grey[200]),
          child: const TextField(
            cursorColor: Colors.green,
            decoration: InputDecoration(
              icon: Icon(
                Icons.person,
                color: Colors.green,
              ),
              hintText: "Enter your name",
              enabledBorder: InputBorder.none,
              focusedBorder: InputBorder.none,
            ),
          ),
        ),
        Container(
          alignment: Alignment.center,
          margin: const EdgeInsets.only(left: 20, right: 20, top: 20),
          padding: const EdgeInsets.only(left: 20, right: 20),
          height: 54,
          decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(50), color: Colors.grey[200]),
          child: const TextField(
            cursorColor: Colors.green,
            decoration: InputDecoration(
              icon: Icon(
                Icons.email,
                color: Colors.green,
              ),
              hintText: "Enter Email",
              enabledBorder: InputBorder.none,
              focusedBorder: InputBorder.none,
            ),
          ),
        ),
        Container(
          alignment: Alignment.center,
          margin: const EdgeInsets.only(left: 20, right: 20, top: 20),
          padding: const EdgeInsets.only(left: 20, right: 20),
          height: 54,
          decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(50), color: Colors.grey[200]),
          child: const TextField(
            cursorColor: Colors.green,
            decoration: InputDecoration(
              icon: Icon(
                Icons.phone,
                color: Colors.green,
              ),
              hintText: "Enter pnone number",
              enabledBorder: InputBorder.none,
              focusedBorder: InputBorder.none,
            ),
          ),
        ),
        Container(
          alignment: Alignment.center,
          margin: const EdgeInsets.only(left: 20, right: 20, top: 20),
          padding: const EdgeInsets.only(left: 20, right: 20),
          height: 54,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(50),
            color: Colors.grey[200],
          ),
          child: const TextField(
            cursorColor: Colors.green,
            obscureText: true,
            enableSuggestions: false,
            autocorrect: false,
            decoration: InputDecoration(
              focusColor: Colors.green,
              icon: Icon(
                Icons.vpn_key,
                color: Colors.green,
              ),
              hintText: "Enter Password",
              enabledBorder: InputBorder.none,
              focusedBorder: InputBorder.none,
            ),
          ),
        ),
        GestureDetector(
          onTap: () {
            // Write Click Listener Code Here.
          },
          child: Container(
            alignment: Alignment.center,
            margin: const EdgeInsets.only(left: 20, right: 20, top: 70),
            padding: const EdgeInsets.only(left: 20, right: 20),
            height: 54,
            decoration: BoxDecoration(
              gradient: const LinearGradient(
                  colors: [Colors.green, Colors.greenAccent],
                  begin: Alignment.centerLeft,
                  end: Alignment.centerRight),
              borderRadius: BorderRadius.circular(50),
              color: Colors.grey[200],
            ),
            child: const Text(
              "REGISTER",
              style: TextStyle(color: Colors.white),
            ),
          ),
        ),
        Container(
          margin: const EdgeInsets.only(top: 10),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text("Have Already Member?  "),
              GestureDetector(
                child: const Text(
                  "Login Now",
                  style: TextStyle(color: Colors.green),
                ),
                onTap: () {
                  Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => const LoginScreen(),
                      ));
                },
              )
            ],
          ),
        )
      ],
    )));
  }
}
