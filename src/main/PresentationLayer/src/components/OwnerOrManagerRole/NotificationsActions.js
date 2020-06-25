import React, {useState} from 'react';
import {Table} from 'react-bootstrap'
import {Link} from 'react-router-dom'
import * as theService from '../../services/communication';

window.$id = 0

window.$notifications = []

export async function addNotification(notification, msg_type, username, store){
    var ls = window.$notifications
    window.$notifications = ls.concat([{'id': window.$id, 'msg': notification, 'msg_type': msg_type, 'username': username , 'store': store}])
    window.$id = window.$id + 1
}

export  function removeNotification(notification_id){
    var new_ls = []
    window.$notifications.forEach(noti => {
console.log(noti['id']);
console.log(notification_id);
        if(noti['id'] !== notification_id)
            new_ls.push(noti)
    });
    window.$notifications = new_ls

}

export  function sendAgreementAnswer(event, noti, answer){

    // call anna : handle_appointment_agreement_response(nickname_apointee, store_name, answer: 1= decline, 2 = approve)
    const promise = theService.sendAgreementAnswer(noti['username'], noti['store'], answer ? 2 : 1)
    promise.then((data) => {
        removeNotification(noti['id'])
    });
}
