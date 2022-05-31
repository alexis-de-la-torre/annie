<?php
    include 'defines.php';

    session_start();

    require_once __DIR__ . '/vendor/autoload.php';

    $creds = array(
        'app_id' => getenv("FACEBOOK_APP_ID"),
        'app_secret' => getenv("FACEBOOK_APP_SECRET"),
        'default_graph_version' => 'v13.0',
        'persistent_data_handler' => 'session',
    );

    $conStr = sprintf("pgsql:host=%s;port=%d;dbname=%s;user=%s;password=%s",
        getenv('POSTGRES_HOST') ?? "localhost",
        getenv('POSTGRES_PORT') ?? "5432",
        getenv('POSTGRES_DATABASE') ?? "guard",
        getenv('POSTGRES_USER') ?? "postgres",
        getenv('POSTGRES_PASSWORD') ?? "postgres");

    $facebook = new Facebook\Facebook( $creds );

    $helper = $facebook->getRedirectLoginHelper();

    $oAuth2Client = $facebook->getOAuth2Client();

    if (isset($_GET['state'])) {
        $_SESSION['FBRLH_state']=$_GET['state'];
    }

    if ( isset( $_GET['code'] ) ) {
        try {
            $accessToken = $helper->getAccessToken(getenv("FACEBOOK_REDIRECT_URL"));
        } catch ( Facebook\Exceptions\FacebookResponseException $e ) {
            echo 'Graph returned an error ' . $e->getMessage();
        } catch ( Facebook\Exceptions\FacebookSDKException $e ) {
            echo 'Facebook SDK returned an error ' . $e->getMessage();
        }

        if ( !$accessToken->isLongLived() ) {
            try {
                $accessToken = $oAuth2Client->getLongLivedAccessToken( $accessToken );
            } catch ( Facebook\Exceptions\FacebookSDKException $e ) {
                echo 'Error getting long lived access token ' . $e->getMessage();
            }
        }

        echo '<pre>';
        var_dump( $accessToken );

        $accessToken = (string) $accessToken;

        $pdo = new \PDO($conStr);
        $pdo->setAttribute(\PDO::ATTR_ERRMODE, \PDO::ERRMODE_EXCEPTION);

        $existsStmt = $pdo->prepare("select * from access_tokens where instagram_id = ?");
        $existsStmt->execute([$instagramAccountId]);
        $row = $existsStmt->fetch(PDO::FETCH_ASSOC);

        if (!$row) {
            $stmt = $pdo->prepare("insert into access_tokens (instagram_id, access_token) values (?, ?)");
            $stmt->execute([$instagramAccountId, $accessToken]);
        } else {
            $stmt = $pdo->prepare("update access_tokens set access_token = ? where instagram_id = ?");
            $stmt->execute([$accessToken, $instagramAccountId]);
        }

        echo '<h1>Long Lived Access Token</h1>';
        print_r( $accessToken );
    } else {
        $permissions = [
            'public_profile',
            'instagram_basic',
            'pages_show_list',
            'instagram_manage_insights',
            'instagram_content_publish',

        ];
        $loginUrl = $helper->getLoginUrl(FACEBOOK_REDIRECT_URI, $permissions);

        echo '<a href="' . $loginUrl . '">
                Login With Facebook
            </a>';
    }