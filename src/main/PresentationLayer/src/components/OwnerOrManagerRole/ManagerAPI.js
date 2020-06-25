import React, {useState} from 'react';
import {Container, Row, Col, Button, Jumbotron, Form} from 'react-bootstrap'
import {Link} from 'react-router-dom'
import * as theService from '../../services/communication';



//---------- WHAT AN OWNER CAN DO? ----------//
// Guest actions 
// Subscriber actions - Logout, Open store, View personal purchase history
// Manage stock (4.1) 
// (4.2)
// Appoint additional owner (4.3)
// Appoint additional manager (4.5)
// Edit manager’s permissions (4.6)
// Remove a store manager (4.7)
// View store’s purchase history (4.10)

// Manage store (5.1) (MANAGER)


class ManagerAPI extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            managedStores: [],
            store: "",
            permissions: []
        }
        
        // this.setPermissions = this.setPermissions.bind(this);
        this.logoutHandler = this.logoutHandler.bind(this);
    }

    // setPermissions = async (permissions) =>{
    //   this.state.pe = permissions; 
    // }

    hasPermission = (permission) =>{
      return this.state.permissions.includes(permission);
    }


    logoutHandler = async () =>{
        const promise = theService.logout(); // goes to register.js and sends to backend
        promise.then((data) => {
          alert(data["msg"]);
            this.props.history.push("/");
        });
    };

    // this function automatically occures once the window opens
    componentDidMount = () => {
        const promise = theService.fetchManagedStores();  // goes to communication.js and sends to server
        promise.then((data) => {
            if(data != null){
                if (data["data"].length > 0){   // if there are owned stores
                    this.setState({managedStores: data["data"], store: data["data"][0]})
                    const promise2 = theService.fetchManagerPermissions(this.state.store);  // goes to communication.js and sends to server
                    promise2.then((data) => {
                        this.setState({permissions: data["data"]});
                    });
                }
                else{
                    alert([data["msg"]]);       // no owned stores, array is empty
                }
            }
        });

    }

    permissionsHandler = () =>{
      const promise2 = theService.fetchManagerPermissions(this.state.store);  // goes to communication.js and sends to server
      promise2.then((data) => {
          // alert(data);
          this.setPermissions(data["data"]);
      });
    }

    render(){
        return(
            <Container id='container' style={{width: this.props["screenWidth"], height: this.props["screenHeight"]}} >
                <Jumbotron id='jumbotron' fluid>
                    <Row>
                        <Col />
                        <Col xs={7}>
                            <h1 style={{textAlign: "center"}}>Welcome Dear Manager!</h1>
                        </Col>
                        <Col>
                        <Link to='/logout'>
                            <Button variant="dark" id="logout" onClick={this.logoutHandler}>Logout</Button>
                        </Link>
                        </Col>
                    </Row>
                </Jumbotron>
                
                <Form.Group id='form-group' controlId="stores_ControlSelect2" onChange={ event => {this.setState({selectedStore: event.target.value})}}>
                <Form.Label id='form-label'>Please choose a store:</Form.Label>
                <Form.Control id='form-select' as="select">
                    {this.state.managedStores.map(store => (
                        
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

                    {/* opptional actions for manager - according to his permissions */}

                    { this.hasPermission(1) ? <Button id='manage-inv' variant="secondary" size="lg" block as={Link} to={{pathname: "/manageinventory/" + this.state.store, 
                                                                                                        store: this.state.store, props: this.props}} >
                                                  Manage Inventory
                                              </Button>
                                        : null }   

                    {/* { this.hasPermission(3) ? <Button variant="secondary" size="lg" block as={Link} to={{pathname: "/appointowner", 
                                                                                                        store: this.state.store, props: this.props}}>
                                                  Appoint Additional Owner
                                              </Button>
                                        : null }   */}
                    { this.hasPermission(5) ? <Button id='appoint-manager' variant="secondary" size="lg" block as={Link} to={{pathname: "/appointmanager", 
                                                                                                        store: this.state.store, props: this.props}}>
                                          Appoint Additional Manager
                                      </Button>
                                      : null }  

                    { this.hasPermission(6) ? <Button id='edit-perm' variant="secondary" size="lg" block as={Link} to={{pathname: "/editpermissions", 
                                                                                                        store: this.state.store, props: this.props}}>
                                            Edit Manager’s Permissions
                                        </Button>
                                        : null }  

                    { this.hasPermission(7) ? <Button id='remove-manager' variant="secondary" size="lg" block as={Link} to={{pathname: "/removemanager", 
                                                                                                        store: this.state.store, props: this.props}}>
                                            Remove A Store Manager
                                        </Button>
                                        : null }  


                    { this.hasPermission(10) ? <Button id='view-purchase-hist' variant="secondary" size="lg" block as={Link} to={{pathname: "/storehistory", 
                                                                                                     store: this.state.selectedStore, props: this.props}}>
                                            View Store’s Purchase History
                                        </Button>
                                        : null }  

                    { this.hasPermission(2) ? <Button id='manage-policies' variant="secondary" size="lg" block as={Link} to={{pathname: "/managestorepolicies", 
                                                                                                     store: this.state.selectedStore, props: this.props}}>
                                            Manage Store Policies
                                        </Button>
                                        : null }  
                </Row>
            </Container>
        );
    }
    

}

export default ManagerAPI;

    


 