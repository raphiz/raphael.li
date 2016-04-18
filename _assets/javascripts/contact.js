(function ($, console, window) {
    'use strict';

    var CryptoMail = {

        /**
         * Initializes the CryptoMail functionallity
         * @return {undefined}
         */
        init : function () {
            // Check if Web Cryptography API is supported. If not, abort
            if (!window.crypto.getRandomValues) {
                console.log("Web Cryptography API not supported by the Browser!");
                return;
            }

            // Show textbox this is done to hide the area when JS is disabled.
            $('#crypto-container').slideDown();

            // Attach click listener to the show crypto btn
            $('#show-crypto-output').click(CryptoMail.showCrypto);

            // Fetch the public key
            $.get("/key.asc", function (data) {
                CryptoMail.pubkey = data;
            });

        },

        /**
         * This method encrypts the given string and returns its ecrypted representation.
         * @param  {String} msg the message to encrypt
         * @return {String} the encrypted representation of the given msg
         */
        encrypt : function (msg) {
            var openpgp = window.openpgp,
                pubKeys = openpgp.key.readArmored(CryptoMail.pubkey);
            return openpgp.encryptMessage([pubKeys.keys[0]], msg);
        },

        /**
         * This method is executed when pushing the "Hide encrypted text" Button.
         * It basically converts itself back into a "Show encrypted text" Button and unbinds
         * all eventually added listeners.
         * @return {undefined}
         */
        hideCrypto : function () {
            var outField = $('#crypto-text-output'),
                srcField = $('#crypto-text-source'),
                showBtn = $('#show-crypto-output');

            // Hide the output field
            outField.slideUp();

            // Update the label on the Buttonn
            showBtn.text("Show encrypt text");

            // Unbind events from textarea
            srcField.unbind('change');
            srcField.unbind('keyup');

            // clear the value of the output field
            outField.text('');

            // Unbind the event
            showBtn.unbind('click');

            // Bind the click event to the show function
            showBtn.click(CryptoMail.showCrypto);

        },

        /**
         * This method is executed when pushing the "Show encrypted text" Button.
         * It basically converts itself into a "Hide encrypted text" Button
         * @return {undefined}
         */
        showCrypto : function () {

            var outField = $('#crypto-text-output'),
                srcField = $('#crypto-text-source'),
                showBtn = $('#show-crypto-output');

            // encrypt the text and set it as value
            outField.text(CryptoMail.encrypt(srcField.val()));

            // Show the output field
            outField.slideDown();

            // Update the label on the button
            showBtn.text("Hide encrypt text");

            // Update output now on every change
            srcField.change(CryptoMail.onchange);
            srcField.keyup(CryptoMail.onchange);

            // Unbind the event
            showBtn.unbind('click');

            // Bind the click event to the hide function
            showBtn.click(CryptoMail.hideCrypto);
        },

        /**
         * The method which is called every time when something changes in the source text area.
         * @return {undefined}
         */
        onchange : function () {
            $('#crypto-text-output').text(CryptoMail.encrypt($('#crypto-text-source').val()));
        },

        /**
         * This method creates a string like "mailto:user@mail.com" with my email adress
         * @return {String} a string like "mailto:user@mail.com"
         */
        getMailtToAddress : function () {
            var greeting = 'hi',
                host = 'raphael.li',
                sign = String.fromCharCode(64),
                what = "mail",
                addr = what + "to:" + greeting + sign  + host;
            return addr;
        }

    };

    // Initialize cryptomail
    CryptoMail.init();

    // Demystify my E-Mail address....
    $('#mail-contact').attr('href', CryptoMail.getMailtToAddress());

    // Allow easy copy
    $(document).ready(function() {
        $('.copy-text').click(function() {
            if ($('#copy-area').length) {
                $('#copy-area').remove();
            }
            var clickText = $(this).text();
            var area = $('<textarea readonly="true" id="copy-area" />')
                .appendTo($(this))
                .val(clickText)
                .focus();
            if ($(document).width() > 768){
                area.select();
            }
            return false;
        });
        $(':not(.copy-text)').click(function() {
            $('#copy-area').remove();
        });
    });

}(jQuery, console, window));
