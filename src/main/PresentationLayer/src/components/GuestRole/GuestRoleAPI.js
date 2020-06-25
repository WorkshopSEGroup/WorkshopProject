import React, {useState} from 'react';
import {Container, Row, Col, Button, Dropdown, Jumbotron, Form} from 'react-bootstrap'
import {Link} from 'react-router-dom'
import * as theService from '../../services/communication';


// WHAT'S LEFT TO DO HERE:
// Available guest's actions in the Service Layer:
// register - done
// login - almost done (except going back, can add a button. Need to display new page for logged in user)
// display_stores_or_products_info 
// search_products_by,      filter_products_by,     save_products_to_basket
// view_shopping_cart - done, need to decide if products have info to view
// update_shopping_cart
// purchase_products,       confirm_payment



//     // STYLING //
//     btnStyle = {
//         borderRadius: "5px",
//         borderWidth: "1px",
//         borderColor: "rgba(117, 116, 116, 0.3)",
//         margin: "0 5% 0 5%",
//         //backgroundColor: "rgba(84, 148, 103, 0.5)"
//     }


function GuestRoleAPI(props){

    return(

        <Container id='container' style={{width: props["screenWidth"], height: props["screenHeight"]}}>
        <Jumbotron id='jumbotron' fluid>
            <Row>
                <Col />
                <Col xs={7}>
                    <h1 style={{textAlign: "center"}}>Welcome to the Trade Contol Where dreams come true!</h1>
                </Col>
                <Col>
                </Col>
            </Row>
        </Jumbotron>
            
                {/*
                        // for guest only
                        1. register - > now button -> redirect to ./register -> ok
                        2. login - > now button -> redirect to ./login -> ok 

                        // guest and up
                        3. display stores and products info, display stores ->  redirect to ./stores
                        4. search products by + filter products by -> in navbar
                        5. save products to basket -> in shopping cart
                        6. view and update shopping cart -> in shopping cart
                    */}
             
        <Row>
            <Button id='register-btn' variant="secondary" size="lg" block as={Link} to="/register"> Register </Button>
            <Button id='login-btn' variant="secondary" size="lg" block as={Link} to="/login"> Login </Button>
            <Button id='display-store-btn' variant="secondary" size="lg" block as={Link} to="/stores"> Display Stores And Products Information </Button>

        </Row>
        </Container>
    );
}


export default GuestRoleAPI;





