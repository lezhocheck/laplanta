import 'package:flutter/material.dart';
import 'package:laplanta/side_panel_header.dart';
import 'package:laplanta/widgets/app_bar.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key, required this.title});

  final String title;

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  var currentPage = SidePanelSections.home;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: LaplantaAppBar(
        title: widget.title,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const <Widget>[
            Text(
              'You have pushed the button this many times:',
            ),
          ],
        ),
      ),
      drawer: Drawer(
        child: SingleChildScrollView(
            child: Column(
          children: [const SidePanelHeader(), sidePanelList()],
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
              currentPage = SidePanelSections.home;
              return;
            }
            currentPage = section;
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
