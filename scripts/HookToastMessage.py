import frida, sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

jscode = """
Java.perform(function () {
    // Function to hook is defined here
    var MainActivity = Java.use('com.arophix.decompileapk.MainActivity');

    // Whenever button is clicked
    MainActivity.onClick.implementation = function (v) {
        // Show a message to know that the function got called
        send('onClick');

        // Call the original onClick handler
        this.onClick(v);

        // Log to the console that it's done, and we should have the flag!
//        console.log('Done:' + JSON.stringify(this.cnt));
    };
});

Java.perform(function () {
    // Function to hook is defined here
    var MainActivity = Java.use('com.arophix.decompileapk.MainActivity');

    // Whenever button is clicked
    MainActivity.isPhoneRooted.implementation = function (v) {
        // Show a message to know that the function got called
        send("Called - isPhoneRooted()");
        return false;
    };
});
"""

process = frida.get_usb_device().attach('com.arophix.decompileapk')
script = process.create_script(jscode)
script.on('message', on_message)
print('[*] Running CTF')
script.load()
sys.stdin.read()
