import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Table, Button, Accordion, Card, Form, Row} from 'react-bootstrap'
import * as theService from '../../services/communication';


function PersonalPurchaseHistory(props){
  useEffect(() => {
    fetchPersonalPurchaseHistory();
  }, []);


  const [purchaseHistory, setPurchaseHistory] = useState([]); 
  const [stores, setStores] = useState([]); 

  const fetchPersonalPurchaseHistory = async () => {
    const promise = theService.fetchPersonalPurchaseHistory(); // goes to register.js and sends to backend
    promise.then((data) => {
      if(data["data"].length === 0)
            alert("You don't have any purchases.");
      else{
          setPurchaseHistory(data["data"])
          const list_of_stores = [];
      
          data["data"].forEach(purchase => {
            if(list_of_stores.indexOf(purchase['store_name']) < 0){
              list_of_stores.push(purchase['store_name'])
            }
          });
          setStores(list_of_stores)
      }
      
    });
  };

  return (
    <div style={{width: props["screenWidth"], height: props["screenHeight"]}}>
      <h1 style={{marginTop:"1%"}}>Personal Purchase History</h1>

      <Accordion id='accordion' style={{marginTop:"1%"}}>
        {stores.map(store => (
           <Card id='card'>
           <Card.Header>
           <Accordion.Toggle id='accordion-toggle' as={Button} type="radio" variant="link" eventKey="0">
               Purchases from store {store}
           </Accordion.Toggle>
           </Card.Header>
           <Accordion.Collapse eventKey="0">
           <Card.Body>
             {/*********** Single purchase display ********/}
             {/* purchaseHistory = [{store_name, nickname, date, total_price, products=[{amount, product_name, products_price}]}] */}
             {/* purchase =  {store_name, nickname, date, total_price, products=[{amount, product_name, products_price}]}*/}
             {purchaseHistory.map(purchase => (
                purchase['store_name'] === store ?
                <div style={{marginTop:"1%" , marginLeft: "10%", marginRight: "10%", border: "1px solid", borderColor: "#CCCCCC"}}>
                    <Table id='table' striped bordered hover >
                      <thead>
                          <tr>
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
                                <td>{product["product_name"]}</td>
                                <td>{product["product_price"]}</td>
                                <td>{product["amount"]}</td>
                            </tr>
                          ))
                        }
                      </tbody>
                    </Table>
                    <Form id='form' style={{marginLeft:"3%"}}>
                    <Row><p>Date: {purchase["date"]}</p></Row>
                    <Row><p>Total Price: {purchase["total_price"]}</p></Row>
                    </Form>
                  </div> : null
             ))}
             </Card.Body>
            </Accordion.Collapse>
        </Card>
        ))}
      </Accordion>

      
  </div>
  );
}

export default PersonalPurchaseHistory;