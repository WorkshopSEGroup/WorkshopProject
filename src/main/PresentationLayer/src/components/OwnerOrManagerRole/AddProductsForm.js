import React, {useState, useEffect} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Container, Button, Form, Row} from 'react-bootstrap'
import * as theService from '../../services/communication';
import * as BackOption from '../Actions/GeneralActions/Back'
import { confirmAlert } from 'react-confirm-alert'; 
import 'react-confirm-alert/src/react-confirm-alert.css'; // Import css



function AddProductsForm(props){
  const [productName, setProductName] = useState("");
  const [productPrice, setProductPrice] = useState(null);
  const [productCategory, setProductCategory] = useState("");
  const [productAmount, setProductAmount] = useState(null);
  const [purchaseType, setPurchaseType] = useState(null);

  const addProductHandler = async () =>{
    const promise = theService.addProduct(props.storeName, productName, productPrice, productCategory, productAmount, purchaseType); // goes to register.js and sends to backend
    promise.then((data) => {
      if(data !== undefined){
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
                setPurchaseType(null);
              }
            },
            {
              label: 'Done',
              onClick: () => {BackOption.BackToHome(props.history)}
            }
          ]
        });
      }
      // else{
      //   alert(data["msg"]);
      // }
        

    });
  };

  const detailsFilled = () => {
    if(props.storeName !== "" && productName !== "" && productPrice !== null && productCategory !== "" && productAmount !== null && purchaseType !== null){
      return true;
    }
  }

  return (
      <div style={{width: props["screenWidth"], height: props["screenHeight"]}}>

        <Container>
          <h1>Add a New Product</h1>
          <Form className='add_product'>
            <Form.Label>Choose the product name:</Form.Label>
            <Form.Control id="product-name" value={productName} as="input" required type="text" placeholder="Product name"
            onChange={(event => {
              setProductName(event.target.value)
            })}/>

            <Form.Label>Set the price:</Form.Label>
            <Form.Control id="product-price" value={productPrice} as="input" required type="number" min={0} required placeholder="Product price" 
            onChange={(event => {
              setProductPrice(event.target.valueAsNumber)
            })}/>
          
            <Form.Label>Enter the category:</Form.Label>
            <Form.Control id="product-category" value={productCategory} as="input" required type="text" placeholder="Category" 
            onChange={(event => {
              setProductCategory(event.target.value)
            })}/>
          
            <Form.Label>Enter the amount:</Form.Label>
            <Form.Control id="product-amount" value={productAmount} as="input" required type="number" min={0} placeholder="Product amount" 
            onChange={(event => {
              setProductAmount(event.target.valueAsNumber)
            })}/>

            <Form.Label>Enter the purchase type:</Form.Label>
            <div key={`inline-checkbox`} className="mb-3" style={{ border: "1px solid", borderColor: "#CCCCCC"}}>
              <div style={{marginLeft:"2%"}}>
                <Row><Form.Check inline label="Immidiate Purcahse" type="radio" id={`immidiate-purchase`} name="formHorizontalRadios" onChange={(event => {setPurchaseType(0)})} value={purchaseType}/></Row>
                <Row><Form.Check inline label="Auction Purchase" type="radio" id={`auction-purchase`} name="formHorizontalRadios" onChange={(event => {setPurchaseType(1)})} value={purchaseType}/></Row>
                <Row><Form.Check inline label="Lottery Purchase" type="radio" id={`lottery-purchase`} name="formHorizontalRadios" onChange={(event => {setPurchaseType(2)})} value={purchaseType}/></Row>
              </div>
            </div>
            {/* <Form.Check type="checkbox" label="Add Discount Type" onChange={handleShowDiscount} style={{position: "relative", right: "43%"}}/> */}

            {/* <ShowDiscount showDiscount={showDiscount} setDiscountType={setDiscountType} discountType={discountType} setDiscountPercentage={setDiscountPercentage} /> */}
            
          </Form>
          <Button variant="dark" id="open-store-button" disabled={!detailsFilled()} onClick={addProductHandler}>Add Product!</Button>
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