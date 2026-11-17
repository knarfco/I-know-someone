<?php
// Receives the service checklist from /plan/checklist/ and emails it.
// A copy of every submission is also saved in /submissions/ (web access blocked by its .htaccess),
// so answers are never lost even if email delivery fails.

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

$TO = '__CHECKLIST_TO__';

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'POST only']);
    exit;
}

$raw = file_get_contents('php://input', false, null, 0, 300000);
$data = json_decode($raw ?: '', true);
if (!is_array($data)) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => 'Bad request']);
    exit;
}

// Honeypot: bots fill hidden fields; pretend success and do nothing.
if (!empty($data['website'])) {
    echo json_encode(['ok' => true]);
    exit;
}

function clean_line($s, $max) {
    $s = is_string($s) ? $s : '';
    $s = strip_tags($s);
    $s = preg_replace('/[\r\n\t]+/', ' ', $s);
    return mb_substr(trim($s), 0, $max);
}

$name = clean_line($data['name'] ?? '', 80);
$summary = is_string($data['summary'] ?? null) ? mb_substr(strip_tags($data['summary']), 0, 120000) : '';
$counts = is_array($data['counts'] ?? null) ? $data['counts'] : [];
$c = function ($k) use ($counts) { return (int)($counts[$k] ?? 0); };

if ($summary === '') {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => 'Empty checklist']);
    exit;
}

$when = date('Y-m-d H:i:s T');
$body = "Service checklist submitted" . ($name !== '' ? " by $name" : '') . "\n"
      . "Sent: $when\n"
      . "We do it: " . $c('do') . " | Sub / team: " . $c('sub') . " | Not for us: " . $c('no') . " | Open: " . $c('open') . "\n"
      . str_repeat('-', 60) . "\n\n"
      . $summary . "\n";

// Save a copy first.
$dir = __DIR__ . '/submissions';
if (!is_dir($dir)) {
    @mkdir($dir, 0750, true);
}
$file = $dir . '/checklist-' . date('Ymd-His') . '-' . bin2hex(random_bytes(3)) . '.txt';
$saved = @file_put_contents($file, $body) !== false;

// Email it. Hostinger expects the From address to be on this site's own domain.
$host = strtolower(preg_replace('/[^a-z0-9.\-]/i', '', $_SERVER['HTTP_HOST'] ?? 'localhost'));
$host = preg_replace('/^www\./', '', $host);
$from = 'no-reply@' . $host;
$subject = 'Everglades service checklist' . ($name !== '' ? " from $name" : '');
$headers = "From: Everglades Website <$from>\r\n"
         . "Reply-To: $from\r\n"
         . "MIME-Version: 1.0\r\n"
         . "Content-Type: text/plain; charset=UTF-8\r\n";
$sent = @mail($TO, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers, '-f' . $from);

echo json_encode(['ok' => ($sent || $saved), 'emailed' => $sent, 'saved' => $saved]);
