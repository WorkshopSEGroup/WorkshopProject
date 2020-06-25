import React, {useState} from 'react';
import {Container, Row, Col, Button, Dropdown, Jumbotron, Form} from 'react-bootstrap'
import {Link, Redirect, Router} from 'react-router-dom'
import * as theService from '../../services/communication';
import * as theWebsocket from '../../services/Notifications';


// WHAT A SUBSCRIBER CAN DO?
// Guest actions - display_stores_or_products_info, search_products_by, view_shopping_cart, update_shopping_cart, purchase_products
//
// Logout (3.1)
// Open store (3.2)
// View personal purchase history (3.7)


class SubscriberAPI extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            searchOption: 0,
            searchInput: '',
            categories: [],

        };

      this.byNameHandler = this.byNameHandler.bind(this);
      this.byKeywordHandler = this.byKeywordHandler.bind(this);
      this.byCategoryHandler = this.byCategoryHandler.bind(this);
      this.searchInputHandler = this.searchInputHandler.bind(this);
      this.fetchCategories = this.fetchCategories.bind(this);
      this.logoutHandler = this.logoutHandler.bind(this);
      this.logoutHandler = this.logoutHandler.bind(this);
    }

    byNameHandler = () =>{
        this.setState({searchOption: 1})
    };
    byKeywordHandler = () =>{
        this.setState({searchOption: 2})
    };
    byCategoryHandler = (input) =>{
        this.setState({searchOption: 3, searchInput: input})
    };
    searchInputHandler = (event) =>{
        this.setState({searchInput: event.target.value})
    }

    // for the search functionality
    fetchCategories = async () =>{
        const promise = theService.getCategories(); // goes to register.js and sends to backend
        promise.then((data) => {this.setState({categories: data["data"]})})
    }

    logoutHandler = async () =>{
        const promise = theService.logout(); // goes to register.js and sends to backend
        promise.then((data) => {
          alert(data["msg"]);
            theWebsocket.logout()
            this.props.history.push("/");
        });
    };

    render(){
        return(
            <Container id='container' style={{width: this.props["screenWidth"], height: this.props["screenHeight"]}}>
                <Jumbotron id='jumbotron' fluid>
                    <Row>
                        <Col />
                        <Col xs={7}>
                            <h1 style={{textAlign: "center"}}>Welcome Dear Subscriber!</h1>
                        </Col>
                        <Col>
                        <Link to='/logout'>
                            <Button variant="dark" id="logout" onClick={this.logoutHandler}>Logout</Button>
                        </Link>
                        </Col>
                    </Row>
                </Jumbotron>
                
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
                </Row>
            </Container>
        );
    }
   

}

export default SubscriberAPI;