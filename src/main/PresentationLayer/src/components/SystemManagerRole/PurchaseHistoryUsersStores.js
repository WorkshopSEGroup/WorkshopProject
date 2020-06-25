import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import {BrowserRouter as Link} from 'react-router-dom'
import {Container, Row, Col, Button, Form, Table} from 'react-bootstrap'
import * as theService from '../../services/communication';
import * as BackOption from '../Actions/GeneralActions/Back';


function PurchaseHistoryUsersStores(props){

//   const [userPurchaseHistory, setUserPurchaseHistory] = useState([]);
//   const [storePurchaseHistory, setStorerPurchaseHistory] = useState([]); 
  const [purchaseHistory, setPurchaseHistory] = useState([]); 
  const [userInput, setUserNameInput] = useState('');
  const [storeNameInput, setStoreNameInput] = useState('');
  const [choice, setChoice1] = useState(0);
  const [selectedCoice, setSelectedChice] = useState('')

  const setChoice = (c) =>{
    if(c === 1)
      setStoreNameInput('');
    else setUserNameInput('');
    setChoice1(c)
  }

  const userInputHandler = (event) =>{
    setUserNameInput(event.target.value);
    setChoice(1);

  };


  const storeNameInputHandler = (event) =>{
    setStoreNameInput(event.target.value);
    setChoice(2);
  };

  const resetFields = () =>{
    setChoice(0)
    setUserNameInput('')
    setStoreNameInput('')
  }

  const onViewHandler = () =>{
     var promise = null;
      if(choice === 1){ // user
        setSelectedChice('user')
         promise = theService.fetchUserPurchaseHistory(userInput); // goes to register.js and sends to backend
      }
      else{ // store
        setSelectedChice('store')
        promise = theService.SystemManagerfetchStorePurchaseHistory(storeNameInput); // goes to register.js and sends to backend
      }

      promise.then((data) => {
        if(data['data'] === null)
          alert(data['msg'])
        else{
          alert(data['msg'])
          setPurchaseHistory(data["data"]);
          resetFields()
        }
    })
  };

  return (
      <div style={{width: props["screenWidth"], height: props["screenHeight"]}}>
        <h1>Purchase History</h1>

        <h4 style={{marginTop:"2%"}}>Please select an option:</h4>
        <div key={`inline-checkbox`} className="mb-3" style={{ marginRight:"25%", marginLeft:"25%",  border: "1px solid", borderColor: "#CCCCCC"}}>
            <div style={{marginLeft:"4%"}}>
            <Row style={{marginTop: "1.5%"}}>
                <Form.Label column  sm="6" style={{left: "-8.5%"}}>
                    <Form.Check type="radio" label="View users’ purchase history"  name="purchase-radio" id="purchase-radio-1" onChange={() => {setChoice(1)}} checked={choice === 1}/>
                </Form.Label>
                <Col sm="6" style={{left: "-8%"}}>
                    <Form.Control type="text" id="purchase-username" value={userInput} placeholder="User name" disabled={choice !== 1} onChange={userInputHandler} className="user_name"/>
                </Col>
            </Row>
            <Row style={{marginTop: "1.5%"}}>
                <Form.Label column  sm="6" style={{left: "-8%"}}>
                    <Form.Check type="radio" label="View stores’ purchase history" name="purchase-radio"id="purchase-radio-2" onChange={() => {setChoice(2)}} checked={choice === 2}/>
                </Form.Label>
                <Col sm="6" style={{left: "-8%", marginBottom:"2%"}}>
                    <Form.Control type="text" id="purchase-storename" value={storeNameInput} placeholder="Store name" disabled={choice !== 2} onChange={storeNameInputHandler} className="store_name"/>
                </Col>
            </Row>
            </div>

            <div style={{marginTop:"1%" , marginLeft: "3%", marginRight: "3%"}}>
             <Form id='form'>
                 <Form.Group as={Row} style={{marginRight:"1%" , marginLeft: "1%"}}>

                 <div><Button variant="dark" id="purchase-view" disabled={choice === 0 || (storeNameInput === '' && userInput === '')} onClick={onViewHandler}>View</Button></div>
                 <div style={{marginLeft:"1%"}}> <Button variant="dark" id="back-btn" onClick={event => BackOption.BackToHome(props)}>Back</Button></div>
                 </Form.Group>
             </Form>
            </div>

        </div>

        

         {/* display list of purchases */}
         {purchaseHistory.length !== 0 ?
         <div style={{marginTop:"3%" , marginLeft: "10%", marginRight: "10%"}}>
           <h4>Search results for {selectedCoice} {selectedCoice === 'user' ? purchaseHistory[0]['nickname'] : purchaseHistory[0]['store_name']}:</h4> 
         </div>: null}
        <div style={{marginTop:"1%" , marginLeft: "5%", marginRight: "5%"}}>
         {purchaseHistory.map(purchase => (
                // purchase['store_name'] === store ?
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
                    <Form id='form-2' style={{marginLeft:"3%"}}>
                    <Row><p>Buyer: {purchase["nickname"]}</p></Row>
                    <Row><p>Store name: {purchase["store_name"]}</p></Row>
                    <Row><p>Date: {purchase["date"]}</p></Row>
                    <Row><p>Total Price: {purchase["total_price"]}</p></Row>
                    </Form>
                </div>
                  //  : null
             ))}

        </div>
      </div>
  );
}

export default PurchaseHistoryUsersStores;