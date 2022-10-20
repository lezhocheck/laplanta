db.auth('admin', 'password');
db = db.getSiblingDB('laplanta');
db.createCollection('users');
