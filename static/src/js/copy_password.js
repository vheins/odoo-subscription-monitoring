odoo.define('subscription_monitoring.copy_password', function (require) {
    "use strict";

    var rpc = require('web.rpc');
    var Dialog = require('web.Dialog');
    var core = require('web.core');
    var _t = core._t;

    // Bind copy button in reveal wizard
    $(document).on('click', '.o_copy_to_clipboard', function (ev) {
        ev.preventDefault();
        // find the password input inside the modal
        var $modal = $(this).closest('.o_dialog');
        var $input = $modal.find('input[name="password"]');
        if ($input.length) {
            var text = $input.val();
            // copy to clipboard
            navigator.clipboard && navigator.clipboard.writeText(text).then(function () {
                Dialog.alert(null, _t('Password copied to clipboard'));
            }).catch(function () {
                Dialog.alert(null, _t('Unable to copy to clipboard. Please copy manually.'));
            });
        }
    });

    // For list/tree: attach handler to buttons with class o_copy_password
    $(document).on('click', '.o_copy_password', function (ev) {
        ev.preventDefault();
        var $btn = $(this);
        var res_id = $btn.data('res-id');
        if (!res_id) {
            Dialog.alert(null, _t('No credential id'));
            return;
        }
        // call RPC to retrieve password and log copy
        rpc.query({
            model: 'sm.credential',
            method: 'read',
            args: [[res_id], ['password']],
        }).then(function (result) {
            var pwd = (result && result[0] && result[0].password) || '';
            // log the copy action
            rpc.query({
                model: 'sm.credential',
                method: 'rpc_log_copy',
                args: [[res_id]],
            }).then(function () {
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    navigator.clipboard.writeText(pwd).then(function () {
                        Dialog.alert(null, _t('Password copied to clipboard'));
                    }).catch(function () {
                        Dialog.alert(null, _t('Unable to copy to clipboard. Please copy manually.'));
                    });
                } else {
                    // fallback: show modal with password
                    Dialog.alert(null, _t('Password:') + ' ' + pwd);
                }
            }).catch(function (err) {
                Dialog.alert(null, _t('Unable to log copy action: ') + err.message);
            });
        }).catch(function (err) {
            Dialog.alert(null, _t('Unable to read credential: ') + err.message);
        });
    });
});
