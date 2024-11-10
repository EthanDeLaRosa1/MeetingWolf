<?php
require_once 'vendor/autoload.php'; // Ensure composer installed all dependencies

session_start();

// Debugging outputs
echo "Session started.<br>";
echo "Client created.<br>";

$client = new Google\Client();
$client->setAuthConfig('/home/bitnami/Oauth.json');
echo "Auth config set.<br>";

$client->setRedirectUri('https://dashboard.meetingwolf.com/oauth2callback.php');
$client->addScope(Google\Service\Calendar::CALENDAR);
$client->setAccessType('offline'); // For refreshing the access token
$client->setPrompt('consent');

// Handle OAuth callback
if (!isset($_GET['code'])) {
    $auth_url = $client->createAuthUrl();
    echo "No code found in the URL. Redirecting to auth URL: <a href='" . $auth_url . "'>$auth_url</a><br>";
    header('Location: ' . filter_var($auth_url, FILTER_SANITIZE_URL));
    exit();
} else {
    $token = $client->fetchAccessTokenWithAuthCode($_GET['code']);
    $_SESSION['access_token'] = $token;
    header('Location: dashboard.php');
}
?>
