import 'package:flutter/material.dart';

class LaplantaAppBar extends StatelessWidget implements PreferredSizeWidget {
  const LaplantaAppBar({super.key, required this.title});

  final String title;

  @override
  Widget build(BuildContext context) {
    return AppBar(
      centerTitle: true,
      title: Row(
        children: [
        const Icon(Icons.spa, size: 20),
        const SizedBox(width: 10),
        Text(title)
      ]));
  }

  @override
  Size get preferredSize => const Size.fromHeight(60.0);
}
