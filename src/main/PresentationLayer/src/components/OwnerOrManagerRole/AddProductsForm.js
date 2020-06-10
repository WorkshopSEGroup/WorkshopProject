import React, {useState, useEffect} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import {BrowserRouter as Router, Switch, Route, Link} from 'react-router-dom'
import {Container, Row, Col, Button, Dropdown, Jumbotron, Form} from 'react-bootstrap'
import * as theService from '../../services/communication';

import { confirmAlert } from 'react-confirm-alert'; 
import 'react-confirm-alert/src/react-confirm-alert.css'; // Import css



function AddProductsForm(props){
  useEffect(() => {
    console.log(props);
    setStoreName(props.storeName);
    // setShowAddFormFunction(props.showForm);
  }, []);

  const [storeName, setStoreName]= useState("");
  // const [showAddFormFunction, setShowAddFormFunction]= useState();

  const [productName, setProductName] = useState("");
  const [productPrice, setProductPrice] = useState();
  const [productCategory, setProductCategory] = useState("");
  const [productAmount, setProductAmount] = useState();
  const [purchaseType, setPurchaseType] = useState(0);
  // const [discountType, setDiscountType] = useState(0);
  // const [discountPercentage, setDiscountPercentage] = useState(0);
  // const [showDiscount, setShowDiscount] = useState(false)

  // const handleShowDiscount = async () => {
  //   if(showDiscount){
  //     setShowDiscount(false);
  //     setDiscountType(0);
  //     setPurchaseType(0);
  //     setDiscountPercentage(0);
  //   }
  //   else{
  //     setShowDiscount(true);
  //   }
  // }

  const addProductHandler = async () =>{
    const promise = theService.addProduct(storeName, productName, productPrice, productCategory, productAmount, purchaseType); // goes to register.js and sends to backend
    promise.then((data) => {

        confirmAlert({
          title: data["msg"],
          buttons: [
            {
              label: 'Add another product',
              onClick: () => { // reset the form in order to add another product
                setProductName("");
                setProductPrice("");
                setProductCategory("");
                setProductAmount("");
                // setDiscountType(0);
                setPurchaseType(0);
                // setDiscountPercentage(0);
              }
            },
          {
            label: 'Done',
            onClick: () => alert('Click No')  //TODO - add an option to go back (need to disable addProductForm)
          }
        ]
      });

    });
  };


  return (
      <div style={{width: props["screenWidth"], height: props["screenHeight"]}}>

        <Container>
          <h1>Add a New Product</h1>
          <Form className='add_product'>
            <Form.Label>Choose the product name:</Form.Label>
            <Form.Control id="product-name" value={productName} required type="text" placeholder="Product name"
            onChange={(event => {
              setProductName(event.target.value)
            })}/>

            <Form.Label>Set the price:</Form.Label>
            <Form.Control id="product-price" value={productPrice} required type="text" required placeholder="Product price" 
            onChange={(event => {
              setProductPrice(event.target.value)
            })}/>
          
            <Form.Label>Enter the category:</Form.Label>
            <Form.Control id="product-category" value={productCategory} required type="text" placeholder="Category" 
            onChange={(event => {
              setProductCategory(event.target.value)
            })}/>
          
            <Form.Label>Enter the amount:</Form.Label>
            <Form.Control id="product-amount" value={productAmount} required type="text" placeholder="Product amount" 
            onChange={(event => {
              setProductAmount(event.target.value)
            })}/>

            <Form.Label>Enter the purchase type:</Form.Label>

            <div key={`inline-checkbox`} className="mb-3" style={{border: "1px solid", borderColor: "#CCCCCC"}}>
              <Form.Check inline label="Immidiate Purcahse" type="checkbox" id={`immidiate-purchase`} onChange={(event => {setPurchaseType(0)})} />
              <Form.Check inline label="Auction Purchase" type="checkbox" id={`auction-purchase`} onChange={(event => {setPurchaseType(1)})} />
              <Form.Check inline label="Lottery Purchase" type="checkbox" id={`lottery-purchase`} onChange={(event => {setPurchaseType(2)})}/>
            </div>

            {/* <Form.Check type="checkbox" label="Add Discount Type" onChange={handleShowDiscount} style={{position: "relative", right: "43%"}}/> */}

            {/* <ShowDiscount showDiscount={showDiscount} setDiscountType={setDiscountType} discountType={discountType} setDiscountPercentage={setDiscountPercentage} /> */}
            
          </Form>

          <Button variant="dark" id="open-store-button" onClick={addProductHandler}>Add Product!</Button>
        </Container>

      </div>
  );
}

function ShowDiscount(props){
  if(props.showDiscount){
    return(
      <div>
        <Form.Label>Enter the discount type:</Form.Label>
        <div key={`inline-checkbox`} className="mb-3" style={{border: "1px solid", borderColor: "#CCCCCC"}}>
          <Form.Check inline label="Visible Discount" type="checkbox" id={`visible-discount`} onChange={props.setDiscountType(0)} />
          <Form.Check inline label="Shallow Discount" type="checkbox" id={`shallow-discount`} onChange={props.setDiscountType(1)} />
          <Form.Check inline label="Hidden Discount" type="checkbox" id={`hidden-discount`} onChange={props.setDiscountType(2)}/>
        </div>
        
       <Form.Label>Enter the discount percentage:</Form.Label>
        <Form.Control id="discount-type" value={props.discountType} required type="text" placeholder="Please enter valid number"
        onChange={(event => {
          props.setDiscountPercentage(event.target.value)
       })}/>
      </div>
    )
  }
  return null;
}

export default AddProductsForm;