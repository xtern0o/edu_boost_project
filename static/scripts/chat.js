$(document).ready(() => {
    $('#form_send_message').on('submit', (e) => {
        e.preventDefault();
    });


    const socket = io.connect('127.0.0.1:5000');
    message_block.scrollTop = message_block.scrollHeight;

    var getUrl = () => {
        return window.location.href;
    }

    var getUrlParams = (key) => {
        url = getUrl();
        first_step = url.split('?');
        second_step = new Array(first_step[1]);
        let params = new Object();
        for (let i = 0; i < second_step.length; i++) {
            let key_and_value = second_step[i].split('=');
            params[key_and_value[0]] = key_and_value[1];
        }
        return params[key];
    };

    socket.on('connect', function() {
        socket.emit('join_group',
        {
            'group': Number(getUrlParams('chat_id'))
        });
    });


    socket.on('disconnect', function() {
        socket.emit('leave_group',
        {
            'group': Number(getUrlParams('chat_id'))
        });
    });


    $('#send_message_button').on('click', function () {
        socket.emit('send_message_json',
            {
                'message_text': $('#message_text').val(),
                'group_id': Number(getUrlParams('chat_id'))
            });
        $('#message_text').val('');
    });

    socket.on('updateMessage', function (data) {
        let message_block = document.getElementById('message_block');
        let message = `
                <div class="card card-wrapper" style="border: none;">
                    <div class="card-body user-card">
                        <div>
                            <div>
                                <div
                                    class="float-start small-picture"
                                    style="background-image: url(${data['pic_url']})" alt=""></div>
                            </div>
                            <div>
                                <h4 class="user-name-card">${data['sender_name']}</h4>
                            </div>
                            <div>
                                <h6 class="message-card">${data['message']}</h6>
                            </div>
                        </div>
                    </div>
                </div>
        `
        message_block.innerHTML += message;
        message_block.scrollTop = message_block.scrollHeight;
    });

    socket.on('message', function (data) {
        socket.emit({'message_text': 'text'});
    });

});