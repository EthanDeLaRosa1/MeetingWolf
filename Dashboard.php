<?php
require_once 'vendor/autoload.php';

session_start();

if (!isset($_SESSION['access_token'])) {
    header('Location: oauth2callback.php');
    exit();
}

$client = new Google\Client();
$client->setAuthConfig('credentials.json');
$client->setAccessToken($_SESSION['access_token']);

// Create Calendar service
$service = new Google\Service\Calendar($client);

// Example: List the next 10 events in the user's calendar
$calendarId = 'primary';
$optParams = array(
    'maxResults' => 10,
    'orderBy' => 'startTime',
    'singleEvents' => true,
    'timeMin' => date('c'),
);

$results = $service->events->listEvents($calendarId, $optParams);

if (count($results->getItems()) == 0) {
    echo "No upcoming events found.";
} else {
    echo "Upcoming events:<br>";
    foreach ($results->getItems() as $event) {
        $start = $event->start->dateTime;
        if (empty($start)) {
            $start = $event->start->date;
        }
        echo htmlspecialchars($event->getSummary()) . " (" . $start . ")<br>";
    }
}
?>
