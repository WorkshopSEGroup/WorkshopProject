import React, {useState} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import {BrowserRouter as Router, Switch, Route, Link, Redirect} from 'react-router-dom'
import {Container, Row, Col, Button, Dropdown, Jumbotron, Form} from 'react-bootstrap'
import * as theService from '../../services/communication';
import { confirmAlert } from 'react-confirm-alert'; 

// import {connect} from '../../services/Notifications';
// import theNotifications from '../../services/Notifications';
// import {register_new_store, connect} from '../../services/Notifications';
import {useEffect} from '../../services/Notifications';
// import setStorename from '../../services/Notifications';;
// import setUsername from '../../services/Notifications';

import * as theNotifications from '../../services/Notifications';


import * as BackOption from '../Actions/GeneralActions/Back'
// TODO - display a form to enter new store details. send the entered data to server.

class OpenStore extends React.Component {
    constructor(props){
      super(props);
      this.state = {
        storeNameInput: "",
        nickname: "",
      }

      const promise = theService.getNickname();
      promise.then((data) => {
        this.setState({nickname: data['data']})
      })
      // bind handlers
      this.storeNameInputHandler = this.storeNameInputHandler.bind(this);
      this.openStoreHandler = this.openStoreHandler.bind(this);
    }

  storeNameInputHandler = (event) =>{
    this.setState({storeNameInput: event.target.value});
    
  };

  openStoreHandler = async () =>{

    // REAL TIME
    const something = theService.getUserType()
    something.then((data) => {
      if(data["data"] === "OWNER"){
        // Notifications.register_new_store('s2');
        theNotifications.register_new_store('s2');
      }
      else {        // FIRST TIME OWNER
        // <Notifications props={'y', 's'}/>
        // <Notifications setState(state => ({ storename: 's', username: 'y' }));/>

        // Notifications.useState(Username='y');

        // Notifications({Username:'y', Storename: 's'});
       
        theNotifications.init(this.state.nickname, this.state.storeNameInput);

        // Notifications.username = 'y';
        // Notifications.storename = 's';
        // <clientWebsocket my_prop={prop} /> - call to useEffect on class clientWebsocket
        // <clientWebsocket />;
      }
    })

    const promise = theService.openStore(this.state.storeNameInput); // goes to register.js and sends to backend
    promise.then((data) => {
      if(data["data"]){ // store created
            confirmAlert({
              title: data["msg"],
              buttons: [
                  {   label: 'ok',
                      onClick: () => { // reset the form in order to add another product
                      this.props.history.push("./owner")
                  }},
              ]
          });
      }
      else{
        alert(data["msg"]);

      }
    });
  };

  render(){
    return (
      <div style={{width: this.props["screenWidth"], height: this.props["screenHeight"]}}>
        <h1 style={{marginTop:"2%"}}>Open Store</h1>
        <Container style={{marginTop:"2%"}}>
        <Form className='open_store'>
          <Form.Label>Choose a name for your new store:</Form.Label>
          <Form.Control id="open-store-text" value={this.state.storeNameInput} type="text" placeholder="Store name" className="search" onChange={this.storeNameInputHandler}/>
        </Form>

        <Button variant="dark" id="open-store-button" onClick={this.openStoreHandler} style={{marginTop: "1%", marginLeft: "1%"}}>Open!</Button>

        </Container>
        
      </div>
    );
  }
  
}

export default OpenStore;