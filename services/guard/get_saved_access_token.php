<?php
    if ( isset( $_GET['instagram_id'] ) ) {
        $instagram_id = $_GET['instagram_id'];
    } else {
        $instagram_id = "17841452721847268";
    }

    $conStr = sprintf("pgsql:host=%s;port=%d;dbname=%s;user=%s;password=%s",
        getenv('POSTGRES_HOST') ?? "localhost",
        getenv('POSTGRES_PORT') ?? "5432",
        getenv('POSTGRES_DATABASE') ?? "guard",
        getenv('POSTGRES_USER') ?? "postgres",
        getenv('POSTGRES_PASSWORD') ?? "postgres");

    $pdo = new \PDO($conStr);
    $pdo->setAttribute(\PDO::ATTR_ERRMODE, \PDO::ERRMODE_EXCEPTION);

    $stmt = $pdo->prepare("select * from access_tokens where instagram_id = ?");
    $stmt->execute([$instagram_id]);
    $row = $stmt->fetch(PDO::FETCH_ASSOC);

    print_r($row['access_token']);