db.createUser(
{
    user: "puskesmas",
    pwd: "puskesmba",
    roles: [
      { role: "readWrite", db: "puskesmas" }
    ]
});
