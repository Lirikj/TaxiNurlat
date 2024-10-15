<?php
// Проверяем, что данные были отправлены через POST
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Получаем данные из POST-запроса
    $from = $_POST['from'];
    $to = $_POST['to'];

    // Формируем сообщение
    $message = "Заказ такси:\nОткуда: $from\nКуда: $to";

    // Токен вашего бота
    $botToken = "6423951514:AAE848xYBRpAx92gihFxrnWyXr70-ULgev0";
    
    // ID вашего канала (например, @channelusername или ID)
    $chatId = "-1002372625214";

    // URL для отправки сообщения через API Telegram
    $url = "https://api.telegram.org/bot$botToken/sendMessage";

    // Параметры для запроса
    $data = [
        'chat_id' => $chatId,
        'text' => $message
    ];

    // Отправка запроса через POST
    $options = [
        'http' => [
            'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
            'method'  => 'POST',
            'content' => http_build_query($data),
        ],
    ];
    $context  = stream_context_create($options);
    $result = file_get_contents($url, false, $context);

    // Проверка результата
    if ($result === FALSE) {
        echo "Ошибка при отправке!";
    } else {
        echo "Сообщение отправлено!";
    }
}
?>
