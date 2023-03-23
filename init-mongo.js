db.createUser(
    {
        user: "admin",
        pwd: "admin",
        roles: [
            {
                role: "readWrite",
                db: "fastapi"
            }
        ]
    }
);
db.createCollection("secrets");