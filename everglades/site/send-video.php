<?php
// Receives job videos logged on /plan/videos/ and emails them.
// A copy of every submission is also saved in /submissions/ (web access blocked by its .htaccess),
// so no short link is ever lost even if email delivery fails.

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

$TO = 'knarfco@yahoo.com';

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'POST only']);
    exit;
}

$raw = file_get_contents('php://input', false, null, 0, 200000);
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
$videos = is_array($data['videos'] ?? null) ? array_slice($data['videos'], 0, 200) : [];
$fields = ['link' => 'Short link', 'job' => 'Job', 'date' => 'Filmed', 'place' => 'Location', 'type' => 'Type of work', 'notes' => 'Notes'];

$lines = [];
$count = 0;
foreach ($videos as $i => $v) {
    if (!is_array($v)) continue;
    $link = clean_line($v['link'] ?? '', 200);
    if (!preg_match('~^(https?://)?(www\.|m\.)?(youtu\.be/|youtube\.com/)~i', $link)) continue;
    $count++;
    $lines[] = "Video $count";
    foreach ($fields as $k => $label) {
        $val = clean_line($v[$k] ?? '', $k === 'notes' ? 1000 : 200);
        if ($val !== '') $lines[] = "  $label: $val";
    }
    $lines[] = '';
}

if (!$lines) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => 'No YouTube links']);
    exit;
}

$when = date('Y-m-d H:i:s T');
$body = "Job videos logged" . ($name !== '' ? " by $name" : '') . "\n"
      . "Sent: $when\n"
      . "Videos: $count\n"
      . str_repeat('-', 60) . "\n\n"
      . implode("\n", $lines) . "\n";

// Save a copy first.
$dir = __DIR__ . '/submissions';
if (!is_dir($dir)) {
    @mkdir($dir, 0750, true);
}
$file = $dir . '/videos-' . date('Ymd-His') . '-' . bin2hex(random_bytes(3)) . '.txt';
$saved = @file_put_contents($file, $body) !== false;

// Email it. Hostinger expects the From address to be on this site's own domain.
$host = strtolower(preg_replace('/[^a-z0-9.\-]/i', '', $_SERVER['HTTP_HOST'] ?? 'localhost'));
$host = preg_replace('/^www\./', '', $host);
$from = 'no-reply@' . $host;
$subject = 'Everglades job videos (' . $count . ')' . ($name !== '' ? " from $name" : '');
$headers = "From: Everglades Website <$from>\r\n"
         . "Reply-To: $from\r\n"
         . "MIME-Version: 1.0\r\n"
         . "Content-Type: text/plain; charset=UTF-8\r\n";
$sent = @mail($TO, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers, '-f' . $from);

echo json_encode(['ok' => ($sent || $saved), 'emailed' => $sent, 'saved' => $saved, 'count' => $count]);
