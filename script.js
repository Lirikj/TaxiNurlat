function callTaxi() {
    var from = $('#destination_from').val();
    var to = $('#destination_to').val();

    // Проверка на заполненность полей
    if (from === "" || to === "") {
        alert("Пожалуйста, заполните оба поля!");
        return;
    }

    // AJAX-запрос для отправки данных на сервер
    $.ajax({
        url: 'send_order.php',
        type: 'POST',
        data: {
            from: from,
            to: to
        },
        success: function(response) {
            alert("Заказ отправлен в Telegram!");
        },
        error: function(xhr, status, error) {
            alert("Ошибка при отправке заказа!");
        }
    });
}
