import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:laplanta/side_panel_header.dart';
import 'package:laplanta/widgets/app_bar.dart';
import 'package:laplanta/services/api.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:laplanta/main.dart';
import 'package:laplanta/widgets/my_plants.dart';

class HomePage extends ConsumerStatefulWidget {
  const HomePage({super.key, required this.title});

  final String title;

  @override
  ConsumerState<HomePage> createState() => _HomePageState();
}

class _HomePageState extends ConsumerState<HomePage> {
  var currentPage = SidePanelSections.home;
  Map<String, dynamic>? user;

  @override
  void initState() {
    super.initState();
    Api api = ref.read(apiProvider);
    WidgetsBinding.instance.addPostFrameCallback((_) async {
      try {
        var response = await api.dio.get('${Api.connection}/user');
        if (!mounted) return;
        setState(() {
          user = jsonDecode(response.toString())["msg"]["user"];
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
      body: ListView(children: <Widget>[
        Container(
          height: 250,
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              colors: [Colors.black45, Colors.black38],
              begin: Alignment.centerLeft,
              end: Alignment.centerRight,
              stops: [0.5, 0.9],
            ),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: const <Widget>[
                  CircleAvatar(
                      backgroundColor: Colors.white70,
                      minRadius: 60.0,
                      child: Icon(
                        Icons.account_circle,
                        color: Colors.black87,
                        size: 150,
                      )),
                ],
              ),
              Text(
                user?["name"] ?? "-",
                style: const TextStyle(
                  fontSize: 35,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
              Text(
                user?["email"] ?? "-",
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 15,
                ),
              ),
            ],
          ),
        ),
        Column(
          children: <Widget>[
            ListTile(
              title: const Text(
                'Account created',
                style: TextStyle(
                  color: Colors.green,
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              subtitle: Text(
                user?["account_created"] ?? "-",
                style: const TextStyle(
                  fontSize: 18,
                ),
              ),
            ),
            const Divider(),
            ListTile(
              title: const Text(
                'Account confirmed',
                style: TextStyle(
                  color: Colors.green,
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              subtitle: Text(
                user?["account_confirmed"] ?? "-",
                style: const TextStyle(
                  fontSize: 18,
                ),
              ),
            ),
            const Divider(),
            ListTile(
              title: const Text(
                'Phone number',
                style: TextStyle(
                  color: Colors.green,
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              subtitle: Text(
                user?["telephone"] ?? "-",
                style: const TextStyle(
                  fontSize: 18,
                ),
              ),
            ),
            const Divider(),
            ListTile(
              title: const Text(
                'Language',
                style: TextStyle(
                  color: Colors.green,
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              subtitle: Text(
                user?["language"] ?? "English",
                style: const TextStyle(
                  fontSize: 18,
                ),
              ),
            ),
          ],
        )
      ]),
      drawer: Drawer(
        child: SingleChildScrollView(
            child: Column(
          children: [SidePanelHeader(user: user), sidePanelList()],
        )),
      ),
    );
  }

  Widget sidePanelList() {
    return Container(
      padding: const EdgeInsets.only(
        top: 15,
      ),
      child: Column(
        // shows the list of menu drawer
        children: [
          menuItem(SidePanelSections.home, Icons.home),
          menuItem(SidePanelSections.myPlants, Icons.spa),
          menuItem(SidePanelSections.mySensors, Icons.sensors),
          const Divider(),
          menuItem(SidePanelSections.notifications, Icons.notifications),
          const Divider(),
          menuItem(SidePanelSections.logout, Icons.logout),
        ],
      ),
    );
  }

  Widget menuItem(SidePanelSections section, IconData icon) {
    return Material(
      color: currentPage == section ? Colors.grey[300] : Colors.transparent,
      child: InkWell(
        onTap: () {
          Navigator.pop(context);
          setState(() {
            if (section == SidePanelSections.logout) {
              Navigator.pop(context);
            } else if (section == SidePanelSections.myPlants) {
              Navigator.push(
                context,
                MaterialPageRoute(
                    builder: (context) => MyPlantsPage(title: widget.title)),
              );
              currentPage = SidePanelSections.home;
            }
          });
        },
        child: Padding(
          padding: const EdgeInsets.all(15.0),
          child: Row(
            children: [
              Expanded(
                child: Icon(
                  icon,
                  size: 20,
                  color: Colors.black,
                ),
              ),
              Expanded(
                flex: 3,
                child: Text(
                  section.toMessage(),
                  style: const TextStyle(
                    color: Colors.black,
                    fontSize: 16,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

enum SidePanelSections { home, myPlants, mySensors, notifications, logout }

extension StringExtension on String {
  String capitalize() {
    return "${this[0].toUpperCase()}${substring(1).toLowerCase()}";
  }
}

extension ToMessage on SidePanelSections {
  String toMessage() {
    var value = toString().split('.').last;
    var parts = value.split(RegExp(r"(?=[A-Z])"));
    return "${parts[0].capitalize()} ${parts.sublist(1).map((e) => e.toLowerCase()).join(' ')}";
  }
}
