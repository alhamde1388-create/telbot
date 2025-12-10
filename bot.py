<?php
ob_start();

// ========== تنظیمات شما ==========
$API_KEY = '8523460156:AAH65BCdKf2ScI29-oYNYJzuShH1CO6ACfk';  // توکن بات
define('API_KEY', $API_KEY);

$admin = 8030525876;  // آیدی عددی شما
$channel_username = '@Hacking_Filltering';  // یوزرنیم کانال برای عضویت اجباری
$bot_username = '@test27281819bot';  // یوزرنیم بات شما
$support_channel = '@ZChargeBit';  // کانال پشتیبانی

// ========== توابع اصلی ==========
function bot($method, $datas = []) {
    $url = "https://api.telegram.org/bot" . API_KEY . "/" . $method;
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $datas);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    $res = curl_exec($ch);
    if (curl_error($ch)) {
        error_log('Curl error: ' . curl_error($ch));
        return false;
    } else {
        return json_decode($res);
    }
    curl_close($ch);
}

function sendmessage($chat_id, $text, $reply_markup = null) {
    $params = [
        'chat_id' => $chat_id,
        'text' => $text,
        'parse_mode' => "HTML"
    ];
    
    if ($reply_markup) {
        $params['reply_markup'] = $reply_markup;
    }
    
    return bot('sendMessage', $params);
}

function checkChannelMembership($user_id) {
    global $channel_username;
    
    // ابتدا کانال رو به صورت public چک می‌کنیم
    $result = bot('getChatMember', [
        'chat_id' => $channel_username,
        'user_id' => $user_id
    ]);
    
    if ($result && $result->ok) {
        $status = $result->result->status;
        // اگر عضو باشه
        return in_array($status, ['member', 'administrator', 'creator']);
    }
    
    return false;
}

// ========== تابع عضویت اجباری ==========
function forceJoinCheck($chat_id, $message_id = null) {
    global $channel_username;
    
    $is_member = checkChannelMembership($chat_id);
    
    if (!$is_member) {
        $keyboard = [
            'inline_keyboard' => [
                [
                    ['text' => '🔗 عضویت در کانال', 'url' => 'https://t.me/Hacking_Filltering']
                ],
                [
                    ['text' => '✅ عضو شدم', 'callback_data' => 'joined_channel']
                ]
            ]
        ];
        
        $message = "📢 *برای استفاده از ربات، ابتدا در کانال زیر عضو شوید:*\n\n";
        $message .= "🔗 کانال: $channel_username\n";
        $message .= "⚠️ پس از عضویت، دکمه 'عضو شدم' را بزنید.";
        
        sendmessage($chat_id, $message, json_encode($keyboard));
        return false;
    }
    
    return true;
}

// ========== ادامه توابع ==========
function deletemessage($chat_id, $message_id) {
    return bot('deleteMessage', [
        'chat_id' => $chat_id,
        'message_id' => $message_id,
    ]);
}

function sendaction($chat_id, $action) {
    return bot('sendChatAction', [
        'chat_id' => $chat_id,
        'action' => $action
    ]);
}

function forward($KojaShe, $AzKoja, $KodomMSG) {
    return bot('forwardMessage', [
        'chat_id' => $KojaShe,
        'from_chat_id' => $AzKoja,
        'message_id' => $KodomMSG
    ]);
}

function sendphoto($chat_id, $photo, $caption, $reply_markup = null) {
    $params = [
        'chat_id' => $chat_id,
        'photo' => $photo,
        'caption' => $caption,
    ];
    
    if ($reply_markup) {
        $params['reply_markup'] = $reply_markup;
    }
    
    return bot('sendPhoto', $params);
}

function save($filename, $TXTdata) {
    $myfile = fopen($filename, "w") or die("Unable to open file!");
    fwrite($myfile, "$TXTdata");
    fclose($myfile);
}

// ========== تابع پردازش آپدیت ==========
function processUpdate($update) {
    global $admin, $channel_username, $bot_username, $support_channel;
    
    $message = isset($update->message) ? $update->message : null;
    $callback_query = isset($update->callback_query) ? $update->callback_query : null;

    $message_id = isset($message->message_id) ? $message->message_id : null;
    $chat_id = isset($message->chat->id) ? $message->chat->id : null;
    $from_id = isset($message->from->id) ? $message->from->id : null;
    $text = isset($message->text) ? $message->text : null;
    
    @mkdir("data", 0755, true);
    @mkdir("data/$chat_id", 0755, true);
    
    $chatid = isset($callback_query->message->chat->id) ? $callback_query->message->chat->id : $chat_id;
    $data = isset($callback_query->data) ? $callback_query->data : null;
    $name = isset($message->from->first_name) ? $message->from->first_name : '';
    
    $current_chat_id = $chat_id ?: $chatid;

    // پردازش callback queries
    if ($data == 'joined_channel') {
        if (checkChannelMembership($chatid)) {
            sendmessage($chatid, "✅ *تبریک! شما عضو کانال هستید.*\n\nاکنون می‌توانید از ربات استفاده کنید.");
            
            $keyboard = [
                'keyboard' => [
                    ['🎈 دریافت شارژ'],
                    ['👥 زیرمجموعه‌ها', '🔗 لینک دعوت'],
                    ['ℹ️ راهنما', '👤 پروفایل']
                ],
                'resize_keyboard' => true,
                'one_time_keyboard' => false
            ];
            
            sendmessage($chatid, "🎉 به ربات خوش آمدید!\n\nمنوی اصلی:", json_encode($keyboard));
        } else {
            sendmessage($chatid, "❌ *شما هنوز عضو کانال نشده‌اید!*\n\nلطفاً ابتدا در کانال عضو شوید سپس دکمه 'عضو شدم' را بزنید.");
        }
        return;
    }

    //======= پنل ادمین =======//
    $is_admin = ($chatid == $admin || $chat_id == $admin || $from_id == $admin);
    
    if ($is_admin && $text == "/admin") {
        $keyboard = [
            'keyboard' => [
                ['📊 آمار ربات', '👥 لیست کاربران'],
                ['📢 ارسال همگانی', '🔗 اضافه کردن رفرال'],
                ['🚫 بلاک کاربر', '✅ آنبلاک کاربر'],
                ['🔙 بازگشت به منوی اصلی']
            ],
            'resize_keyboard' => true,
            'one_time_keyboard' => false
        ];
        
        sendmessage($chat_id, "🛠️ *پنل مدیریت*\n\nبه پنل مدیریت خوش آمدید!", json_encode($keyboard));
        file_put_contents("data/$chat_id/mode.txt", "admin_panel");
        return;
    }
    
    //======= منوی اصلی کاربران =======//
    if ($text == '/start') {
        // بررسی عضویت در کانال
        if (!checkChannelMembership($chat_id)) {
            forceJoinCheck($chat_id);
            return;
        }
        
        $user = @file_get_contents('Member.txt');
        $members = $user ? explode("\n", $user) : [];
        
        if (!in_array($chat_id, $members)) {
            $add_user = @file_get_contents('Member.txt');
            $add_user .= $chat_id . "\n";
            file_put_contents('Member.txt', $add_user);
            
            @mkdir("data/$chat_id", 0755, true);
            file_put_contents("data/$chat_id/membrs.txt", "0");
            file_put_contents("data/$chat_id/mem.txt", "0");
            file_put_contents("data/$chat_id/nova.txt", "no");
        }
        
        $keyboard = [
            'keyboard' => [
                ['🎈 دریافت شارژ'],
                ['👥 زیرمجموعه‌ها', '🔗 لینک دعوت'],
                ['ℹ️ راهنما', '👤 پروفایل']
            ],
            'resize_keyboard' => true,
            'one_time_keyboard' => false
        ];
        
        sendaction($chat_id, 'typing');
        sendmessage($chat_id, "👋 سلام $name عزیز!\n\nبه ربات دریافت شارژ رایگان خوش آمدید! 😊", json_encode($keyboard));
        return;
    }
    
    // بررسی اگر کاربر بلاک شده
    $penlist = @file_get_contents("data/pen.txt");
    if ($penlist && strpos($penlist, "$from_id") !== false) {
        sendmessage($chat_id, "🚫 شما از ربات بلاک شده‌اید.");
        return;
    }
    
    // پردازش لینک دعوت
    if ($text && strpos($text, '/start') === 0) {
        $parts = explode(' ', $text);
        if (count($parts) > 1) {
            $referrer_id = $parts[1];
            
            if ($from_id == $referrer_id) {
                sendmessage($chat_id, "❌ نمی‌توانید با لینک خودتان عضو شوید!");
                return;
            }
            
            $users = @file_get_contents('users.txt');
            if (strpos($users, "$from_id") !== false) {
                sendmessage($chat_id, "⚠️ شما قبلاً در ربات عضو شده‌اید!");
            } else {
                $add_user = @file_get_contents('users.txt');
                $add_user .= $from_id . "\n";
                file_put_contents('users.txt', $add_user);
                
                $sho = @file_get_contents("data/$referrer_id/mem.txt");
                $getsho = intval($sho) + 1;
                file_put_contents("data/$referrer_id/mem.txt", $getsho);
                
                $sea = @file_get_contents("data/$referrer_id/membrs.txt");
                $getsea = intval($sea) + 1;
                file_put_contents("data/$referrer_id/membrs.txt", $getsea);
                
                @mkdir("data/$from_id", 0755, true);
                file_put_contents("data/$from_id/membrs.txt", "0");
                file_put_contents("data/$from_id/mem.txt", "0");
                file_put_contents("data/$from_id/nova.txt", "no");
                
                sendmessage($chat_id, "🎉 تبریک! شما با دعوت کاربر $referrer_id عضو شدید!");
                sendmessage($referrer_id, "🎊 یک کاربر جدید با لینک دعوت شما عضو شد!");
            }
        }
        return;
    }
    
    // پردازش دکمه‌های منوی اصلی (با بررسی عضویت)
    if ($text == "🎈 دریافت شارژ" || $text == "👥 زیرمجموعه‌ها" || $text == "🔗 لینک دعوت" || 
        $text == "ℹ️ راهنما" || $text == "👤 پروفایل") {
        
        if (!checkChannelMembership($chat_id)) {
            forceJoinCheck($chat_id);
            return;
        }
    }
    
    // ادامه کد مثل قبل... (بقیه توابع رو از سورس قبلی کپی کن)
    // ... [بقیه کدها مثل سورس قبلی]
}

// ========== اجرای اصلی ==========
echo "🤖 ربات شارژساز در حال اجرا...\n";
echo "👤 ادمین: 8030525876 (@Unilel)\n";
echo "🤖 بات: @test27281819bot\n";
echo "📢 کانال اجباری: @Hacking_Filltering\n";
echo "🆘 پشتیبانی: @ZChargeBit\n";
echo "⏹️ برای متوقف کردن: Ctrl+C\n\n";

$last_update_id = 0;

while (true) {
    try {
        $updates = bot('getUpdates', ['offset' => $last_update_id + 1, 'timeout' => 30]);
        
        if ($updates && $updates->ok && !empty($updates->result)) {
            foreach ($updates->result as $update) {
                $last_update_id = $update->update_id;
                processUpdate($update);
            }
        }
        
        sleep(1);
    } catch (Exception $e) {
        echo "❌ خطا: " . $e->getMessage() . "\n";
        sleep(5);
    }
}
?>
