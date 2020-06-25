import React, {useState} from 'react';
import {Container, Row, Col, Button, Dropdown, Jumbotron, Form} from 'react-bootstrap'
import {Link} from 'react-router-dom'
import * as theService from '../../services/communication';
import SubscriberAPI from '../SubscriberRole/SubscriberAPI';
import * as Notifications from './NotificationsActions';
import { AlertList, Alert, AlertContainer } from "react-bs-notifier";
import { MDBNotification,MDBIcon,  MDBContainer ,MDBBtn, toast} from "mdbreact"
import { IoMdNotifications} from "react-icons/io";
import * as theWebsocket from '../../services/Notifications';

// window.$store = "1"

class OwnerAPI extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            ownedStores: [],
            selectedStore: "",
            showNotifications: false
        }
        
      this.logoutHandler = this.logoutHandler.bind(this);
      this.notificationsHandler = this.notificationsHandler.bind(this);
      this.setSelectedStore = this.setSelectedStore.bind(this);


    }

    logoutHandler = async () =>{
        const promise = theService.logout(); // goes to register.js and sends to backend
        promise.then((data) => {
          alert(data["msg"]);
          theWebsocket.logout()
            this.props.history.push("/");
        });
    };

    notificationsHandler = async () =>{
        // alert(window.$notifications)
        this.setState({showNotifications: !this.state.showNotifications})
    };

    componentDidMount = () => {
        const promise = theService.fetchOwnedStores();  // goes to communication.js and sends to server
        promise.then((data) => {
            if(data != null){
                if (data["data"].length > 0){   // if there are owned stores
                    this.setState({ownedStores: data["data"], selectedStore: data["data"][0]})
                }
                else{
                    alert([data["msg"]]);       // no owned stores, array is empty
                }
            }
        });
    }

    setSelectedStore = (store) =>{
        this.setState({selectedStore:store})
    }
    render(){
        return(
            <Container id='container' style={{width: this.props["screenWidth"], height: this.props["screenHeight"]}}>
                <Jumbotron id='jumbotron' fluid>
                    <Row>
                        <Col />
                        <Col xs={7}>
                            <h1 style={{textAlign: "center"}}>Welcome Dear Owner!</h1>
                        </Col>
                        <Col>
                            <div style={{marginLeft:"75%", marginTop:"3%"}}>
                            <Link>
                                <IoMdNotifications id='noti' class="notification-icon-effect" color="black" font-size="40px" onClick={this.notificationsHandler}/>
                                { window.$notifications.length > 0 ?
                                    <div id="ex4">
                                        <span class="p1 fa-stack fa-2x has-badge" data-count={window.$notifications.length}></span>
                                    </div>
                                  : null}
                                </Link>
                            </div>
                        </Col>
                        <Col>
                            <div style={{marginRight:"50%", marginTop:"3%"}}>
                                <Link to='/logout'>
                                    <Button variant="dark" id="logout" onClick={this.logoutHandler}>Logout</Button>
                                </Link>
                            </div>
                        </Col>
                    </Row>
                </Jumbotron>
                
                <Form.Group id='form-group' controlId="stores_ControlSelect2" onChange={ event => {this.setSelectedStore(event.target.value)}}>
                <Form.Label id='form-label'>Please choose a store:</Form.Label>
                <Form.Control id='form-select' as="select">
                    {/* <option value={""} >Select Store</option> */}
                    {this.state.ownedStores.map(store => (
                        <option value={store}>{store}</option>
                    ))}
                </Form.Control>
                </Form.Group>
    
                {/*
                    need options for:
                    // for guest only
                    1. register - > now button -> redirect to ./register -> ok
                    2. login - > now button -> redirect to ./login -> ok 

                    // guest and up
                    3. display stores and products info, display stores ->  redirect to ./stores
                    4. search products by + filter products by -> in navbar
                    5. save products to basket -> in shopping cart
                    6. view and update shopping cart -> in shopping cart

                    // subscriber and up
                    7. purchase shopping cart -> in shopping cart
                    8. open store
                    9. view personal purchase history
                    10. logout - > now button -> redirect to ./login -> ok

                    // shop owner and up
                    11. manage stock
                    12. appoint owner
                    13. appoint manager
                    14. edit permissions
                    15. remove manager
                    16. view store history
                    17. manage store
                */}

                <Row>
                    <Button id='display-store-btn' variant="secondary" size="lg" block as={Link} to="/stores">
                        Display Stores And Products Information
                    </Button>
    
                    <Button id='open-store-btn' variant="secondary" size="lg" block as={Link} to="/openstore">
                        Open Store
                    </Button>
    
                    <Button id='personal-history-btn' variant="secondary" size="lg" block as={Link} to="/history">
                        View Personal Purchase History
                    </Button>

                    <Button id='manage-inv' variant="secondary" size="lg" block as={Link} to={{pathname: "/manageinventory/" + this.state.selectedStore, 
                                                                               store: this.state.selectedStore, props: this.props}} >
                        Manage Inventory
                    </Button>

                    <Button id='appoint-owner' variant="secondary" size="lg" block as={Link} to={{pathname: "/appointowner", 
                                                                               store: this.state.selectedStore, props: this.props}}>
                        Appoint Additional Owner
                    </Button>
                    <Button id='remove-owner' variant="secondary" size="lg" block as={Link} to={{pathname: "/removeowner", 
                                                                               store: this.state.selectedStore, props: this.props}}>
                        Remove Owner
                    </Button>

                    <Button id='appoint-manager' variant="secondary" size="lg" block as={Link} to={{pathname: "/appointmanager", 
                                                                               store: this.state.selectedStore, props: this.props}}>
                        Appoint Additional Manager
                    </Button>

                    <Button id='edit-perm' variant="secondary" size="lg" block as={Link} to={{pathname: "/editpermissions", 
                                                                               store: this.state.selectedStore, props: this.props}}>
                        Edit Manager’s Permissions
                    </Button>

                    <Button id='remove-manager' variant="secondary" size="lg" block as={Link} to={{pathname: "/removemanager", 
                                                                               store: this.state.selectedStore, props: this.props}}>
                        Remove A Store Manager
                    </Button>

                    <Button id='view-purchase-hist' variant="secondary" size="lg" block as={Link} to={{pathname: "/storehistory", 
                                                                             store: this.state.selectedStore, props: this.props}}>
                        View Store’s Purchase History
                    </Button>

                    <Button id='manage-policies' variant="secondary" size="lg" block as={Link} to={{pathname: "/managestorepolicies", 
                                                                               store: this.state.selectedStore, props: this.props}}>
                        Manage Store Policies
                    </Button>


                    { this.state.showNotifications ?

                         <div>
                             <MDBContainer id='container-2' style={{width: "auto", position: "fixed", bottom: "11px", right: "11px", zIndex: 9999}}>
                                { window.$notifications.map(noti => (
                                    <MDBNotification
                                        show
                                        fade
                                        icon="bell"
                                        iconClassName="green-text"
                                        bodyClassName="p-3 font-weight-bold white-text"
                                        className="notification-body"
                                        titleClassName="notification-title"
                                        title="New Message"
                                        message={ noti['msg_type'] === 'agreement' ?
                                                    <div>
                                                        <div>{noti['msg']}</div>
                                                        <div style={{marginTop:"2%"}}>
                                                            <Button variant='dark' onClick={event => Notifications.sendAgreementAnswer(event, noti, true)}>approve</Button>
                                                            <Button variant='dark' onClick={event => Notifications.sendAgreementAnswer(event, noti, true)} style={{marginLeft:"3%"}}>decline</Button>
                                                        </div>
                                                    </div>
                                                    :
                                                    <div>
                                                        <div>{noti['msg']} </div>
                                                        <div style={{marginTop:"2%"}}><Button variant='dark' onClick={event => Notifications.removeNotification(noti['id'])} style={{marginLeft:"3%"}}>ok</Button></div>
                                                    </div>
                                                }

                                    />
                                    ))
                                }
                            </MDBContainer>

                            {/* <AlertContainer>
                                { window.$notifications.map(noti => (
                                    <div>
                                        <Alert id="model" type="success"  show="true" onDismiss={true} timeout={3000}
                                               headline=
                                                        { <div>
                                                            Message:
                                                            <button type="button" class="close" closeLable="close" aria-label="Close" data-dismiss="alert">
                                                                <span aria-hidden="true">&times;</span>
                                                            </button>
                                                          </div>
                                                        }>

                                            hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
                                            {noti['msg']}

                                        </Alert>
                                    </div>
                                ))}
                            </AlertContainer> */}
                         </div>
                         : null}

                </Row>
            </Container>
            
        );
    }
    

}

export default OwnerAPI;