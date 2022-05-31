<?php
    session_start();

    define( 'ENDPOINT_BASE', getenv("FACEBOOK_GRAPH_ENDPOINT_BASE") ?? 'https://graph.facebook.com/v13.0/');

    // accessToken
    $accessToken = getenv("ACCESS_TOKEN");

    // page id
    $pageId = getenv("PAGE_ID");

    // instagram business account id
    $instagramAccountId = getenv("INSTAGRAM_ACCOUNT_ID");