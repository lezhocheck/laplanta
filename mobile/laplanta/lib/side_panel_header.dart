import 'package:flutter/material.dart';

class SidePanelHeader extends StatefulWidget {
  const SidePanelHeader({super.key, required this.user});
  final Map<String, dynamic>? user;

  @override
  State<SidePanelHeader> createState() => _SidePanelHeaderState();
}

class _SidePanelHeaderState extends State<SidePanelHeader> {
  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.green[700],
      width: double.infinity,
      height: 200,
      padding: const EdgeInsets.only(top: 20.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            margin: const EdgeInsets.only(bottom: 10),
            height: 70,
            child: const Icon(Icons.account_circle,
                color: Colors.green, size: 70.0),
          ),
          Text(
            widget.user!["name"].toString(),
            style: const TextStyle(color: Colors.white, fontSize: 20),
          ),
          Text(
            widget.user!["email"].toString(),
            style: TextStyle(
              color: Colors.grey[200],
              fontSize: 14,
            ),
          ),
        ],
      ),
    );
  }
}
