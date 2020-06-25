import React from 'react';
import {Container, Button, Row, Form} from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';
import {BrowserRouter as Router, Switch, Route, Link} from 'react-router-dom'
import * as theService from '../../services/communication';
import * as BackOption from '../Actions/GeneralActions/Back';
import * as theWebsocket from '../../services/Notifications';


class Login extends React.Component{
    constructor(props) {
      super(props);
      this.state = {
        nickname: '',
        password: '',
      };

    this.handleLogin = this.handleLogin.bind(this);
    this.handleEmailChange = this.handleEmailChange.bind(this);
    this.handlePasswordChange = this.handlePasswordChange.bind(this);
  }

  // componentWillUnmount = () =>{

  // }

  handleLogin = event =>{
    event.preventDefault();
        const promise = theService.login(this.state.nickname, this.state.password) // goes to register.js and sends to backend
        promise.then((data) => {
          let is_manager = data["msg"] === "SYS_MANAGER";
          if(!is_manager){
            alert(data["msg"]);
          }
          if(data["data"]){ // if logged in
              theWebsocket.login(this.state.nickname);
              if(is_manager){
                // if system manager - redirect to system manager home page
                this.props.history.push({pathname: '/systemmanager', props: this.props});
              }
              else{
                const userType = theService.getUserType();
                userType.then((data) => {
                  if(data["data"] === "OWNER"){
                      // websocket
                      // theWebsocket.login(this.state.nickname);
                    // if store owner - redirect to subscriber home page
                    this.props.history.push({pathname: '/owner', props: this.props});
                  }
                  else if(data["data"] === "MANAGER"){
                    // if store manager - redirect to subscriber home page
                    this.props.history.push({pathname: '/manager', props: this.props});
                  }
                  else if(data["data"] === "SYSTEMMANAGER"){
                    this.props.history.push({pathname: '/systemmanager', props: this.props});
                  }
                  else{
                    // if subscriber - redirect to subscriber home page
                    this.props.history.push({pathname: '/subscriber', props: this.props});
                  }
                })
              }
            }
            else{
              // user didn't succeed to log in
              this.state.nickname = ''
              this.state.password = ''
              return;
            }
        });
  }

  handleEmailChange(event){
    this.setState({nickname: event.target.value});
  }

  handlePasswordChange(event){
    this.setState({password: event.target.value});
  }

  render(){
    return (

         <div style={{width: this.props["screenWidth"], height: this.props["screenHeight"]}}>
         <div style={{marginTop:"1%"}}>
             <h2>Login </h2>
         </div>
         <div style={{marginTop:"0.5%" , marginLeft: "25%", marginRight: "25%", border: "1px solid", borderColor: "#CCCCCC"}}>
             <Form >
                 <fieldset>
                     <Form.Group as={Row} >
                         <Form.Label as="legend" column sm={6}>
                             Please enter a unique nickname and password:
                         </Form.Label>
                        <Form.Control style={{marginRight:"3%" , marginLeft: "3%"}} type="text" id="email" name="email" placeholder="Nickname" value={this.state.email} onChange={this.handleEmailChange} />
                         <Form.Control style={{marginTop:"1%", marginRight:"3%" , marginLeft: "3%"}} type="password" id="password" name="password" placeholder="Password" value={this.state.password} onChange={this.handlePasswordChange}/>
                     </Form.Group>
                 </fieldset>
                 <Form.Group as={Row} style={{marginRight:"1%" , marginLeft: "1%"}}>
                     <Button type="reset" variant="dark" disabled={this.state.email === "" | this.state.password === ""} onClick={this.handleLogin} to='/'>Login</Button>

                 </Form.Group>
             </Form>
         </div>
         <div style={{marginTop:"1%" , marginLeft: "25%", marginRight: "25%"}}>
             <Form >
                 <Form.Group as={Row} style={{marginRight:"1%" , marginLeft: "1%"}}>
                 <div><Button variant="dark" as={Link} to="./register">Register</Button></div>
                 {/* <div style={{marginLeft:"1%"}}> <Button variant="dark" id="back-btn" onClick={event => BackOption.BackToHome(this.props)}>Back</Button></div> */}
                 </Form.Group>
             </Form>
         </div>

     </div>
         
    );
   
  }
}


export default Login;
