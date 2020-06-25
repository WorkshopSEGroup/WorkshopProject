
import {useState, useEffect} from 'react';
import port from '../App';
import 'bootstrap/dist/css/bootstrap.min.css';
import io from 'socket.io-client';
import * as Notifications from '../components/OwnerOrManagerRole/NotificationsActions';

var socket = {socket: io.connect('http://127.0.0.1:5000', {transports: ["websocket"], autoConnect: true, forceNew: true})};
var nickname = {nickname:''};
var storeName = {storeName:''};
var counter = {counter:0};

export async function init (nick_name, store_name){
  if (!this.counter){
    nickname = {nickName: nick_name};
    // this.nickname = {nickName: nickname};
    storeName = {storeName: store_name};
    console.log("this nickname:" + nickname.nickName);
    // console.log("this nickname:" + this.nickname.nickName);
    console.log("this storename:" + storeName.storeName);
    this.counter = {counter: 1};
    console.log(nickname.nickName + " is connected to server by websocket");
    // console.log(this.nickname.nickName + " is connected to server by websocket");
    await connect();
  }
  return;
}

export const connect = async (host, username) => {
  console.log("nickname= " + nickname.nickName + ", storename= " + storeName.storeName);
  socket.socket.emit("join", {username: nickname.nickName, store: storeName.storeName});
  // socket.socket.emit("join", {username: this.nickname.nickName, store: this.storeName.storeName});
  await setHandlers();
}

export const setHandlers = async () => {
  socket.socket.on("message", (data) => {
    Notifications.addNotification(data['messages'], 'regular', '','')
  });
  socket.socket.on("agreement", (data) => {
    Notifications.addNotification(data['messages'], 'agreement', data['username'],data['store'])
  });
  // socket.socket.on("daily_cut", (data) => {
  //     // TODO - eden should create an update-daily-cut function
  // });
};

export const disconnect = () => {
  socket.socket.emit("unsubscribe", { username: this.nickname.nickname });
}

export const login = (user_name) => {
  socket.socket.emit("login", { username: user_name });
  nickname = {nickName: user_name};
}

export const register_new_store = (username, storename) => {
  console.log("on register store");
  if (counter.counter === 1)
    console.log("call set handlers");
    setHandlers();
  socket.socket.emit("join", { username: username, store:storename });
  nickname = {nickName: username};

  // else
  //   alert("there were'nt init!!")
}

export const logout = () => {
  socket.socket.emit("logout", { username: nickname.nickName });
}

// TODO - add func that cause 'ask_for_daily_cut_event'

