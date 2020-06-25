import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Table, Button, Accordion, Card, Form, Row} from 'react-bootstrap'
import * as theService from '../../services/communication';
import * as BackOption from '../Actions/GeneralActions/Back'


function StorePurchaseHistory(props){
  useEffect(() => {
    setSelectedStore(props.location.store)
    fetchStorePurchaseHistory(props.location.store);
  }, []);


  const [purchaseHistory, setPurchaseHistory] = useState([]); 
  const [store, setSelectedStore] = useState(""); 

  const fetchStorePurchaseHistory = async (store_name) => {
    const promise = theService.fetchStorePurchaseHistory(store_name); // goes to register.js and sends to backend
    promise.then((data) => {
    alert(data["data"])

        if(data["data"].length === 0)
            alert("There are no purchases in store "+ store_name + ".");
        else
            setPurchaseHistory(data["data"])
    });
  };

  return (
    <div style={{width: props["screenWidth"], height: props["screenHeight"]}}>
      <h1 style={{marginTop:"1%"}}>Store Purchase History</h1>

      {/* <Accordion style={{marginTop:"1%"}}> */}
        {/* {stores.map(store => ( */}
           {/* <Card> */}
           {/* <Card.Header> */}
           {/* <Accordion.Toggle as={Button} type="radio" variant="link" eventKey="0"> */}
               {/* Purchases from store {store} */}
           {/* </Accordion.Toggle> */}
           {/* </Card.Header> */}
           {/* <Accordion.Collapse eventKey="0"> */}
           {/* <Card.Body> */}
             {/*********** Single purchase display ********/}
             {/* purchaseHistory = [{store_name, nickname, date, total_price, products=[{amount, product_name, products_price}]}] */}
             {/* purchase =  {store_name, nickname, date, total_price, products=[{amount, product_name, products_price}]}*/}
             {purchaseHistory.map(purchase => (
                purchase['store_name'] === store ?
                <div style={{marginTop:"1%" , marginLeft: "10%", marginRight: "10%", border: "1px solid", borderColor: "#CCCCCC"}}>
                    <Table id='table' striped bordered hover >
                      <thead>
                          <tr>
                              {/* <th>Buier</th> */}
                              <th>Product Name</th>
                              <th>Price</th>
                              <th>Amount</th>
                          </tr>
                      </thead>
                      <tbody>
                        {
                          // product = {product_name, product_price, amount}
                          purchase["products"].map(product => (
                            <tr>
                                {/* <td>{product["nickname"]}</td> */}
                                <td>{product["product_name"]}</td>
                                <td>{product["product_price"]}</td>
                                <td>{product["amount"]}</td>
                            </tr>
                          ))
                        }
                      </tbody>
                    </Table>
                    <Form id='form' style={{marginLeft:"3%"}}>
                    <Row><p>Buyer: {purchase["nickname"]}</p></Row>
                    <Row><p>Date: {purchase["date"]}</p></Row>
                    <Row><p>Total Price: {purchase["total_price"]}</p></Row>
                    </Form>
                  </div> : null
             ))}
             {/* </Card.Body> */}
            {/* </Accordion.Collapse> */}
        {/* </Card> */}
        {/* ))} */}
      {/* </Accordion> */}

      {/* <Button style={{marginTop: "1%"}} variant="dark" id="back-btn" onClick={event => BackOption.BackToHome(props)}>Back</Button> */}
      
  </div>
  );
}

export default StorePurchaseHistory;