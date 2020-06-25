import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import {BrowserRouter as Router, Route, Link } from 'react-router-dom'
// import { browserHistory } from "react-router";
import {Container, Button, Table, Form, InputGroup, FormControl} from 'react-bootstrap'
import * as theService from '../../../services/communication';
// import * as BackOption from '../GeneralActions/Back'


function StoreProducts(props) {
  useEffect(() => {
    setStoreName(props.storeName);
    console.log(storeName);
    fetchStoreProducts(props.storeName);
    // setHistory(useHistory());
  }, []);

  // const [history, setHistory]= useState('');
  const [storeName, setStoreName] = useState('');
  const [storeProducts, setStoreProducts] = useState([]);
  const [productAmount, setProductAmount] = useState(0);
  const [showAddToCart, setShowAddToCart] = useState(false);
  const [amountValidated, setAmountValidated] = useState(true);

  const onButtonClickHandler = () => {
    alert('Product info Product info')
    //TODO, ADD OPTION TO VIEW PRICE, POLICIES
  };

  const addToCartHandler = async (product_name) => {
    // need - store_name, product_name, product_amount
    const promise = theService.addToProductsCart(storeName, product_name , productAmount)
    promise.then((data => {
      if(data != null){
        if(data["msg"] != null){
          alert(data["msg"]);
        }
      }
    }))
  }

  const showAddToCartHandler = async () => {
    if(showAddToCart){
      setShowAddToCart(false);
    }
    else{
      setShowAddToCart(true);
    }
  }

  const fetchStoreProducts = async (storeName) => {
    const promise = theService.displayStoresProducts(storeName)
    promise.then((data) => {
      if(data != null){
        if (data["data"] != null && data["data"].length > 0){   // if there are stores to display
          setStoreProducts(data["data"]);
        }
        else{
          alert(data["msg"]);      // no products to display
        }
      }
  });
};

  return (
    <div style={{width: props["screenWidth"], height: props["screenHeight"]}}>
      <div>
        <h1>{storeName} - Products</h1>
      </div>

      <div style={{marginTop: "3%", marginLeft: "1%", marginRight: "1%"}}>
        <Table id='table' striped bordered hover >
          <thead>
              <tr>
                  <th>Product Name</th>
                  <th>Price</th>
                  <th>Category</th>
                  <th>Amount</th>
                  <th>
                    <Form.Check id="add-to-cart-checkbox" type="checkbox" label="Add To Cart" onChange={showAddToCartHandler} />
                  </th>
              </tr>
          </thead>
          <tbody>
              {
                storeProducts.map(storeProduct => (
                  <tr>
                      <td>{storeProduct["name"]}</td>
                      <td>{storeProduct["price"]}</td>
                      <td>{storeProduct["category"]}</td>
                      <td>{storeProduct["amount"]}</td>
                      <td>
                        {
                          showAddToCart ? 
                          <div>
                              <InputGroup className="mb-3">
                                <Form.Control id="product-amount" required as="input" type="number" min={0} max={storeProduct["amount"]} placeholder="Product amount" style={{width:"1px"}}
                                  onChange={(event => {
                                    try{
                                      let value = event.target.valueAsNumber;
                                      if(value > 0 && value <= storeProduct["amount"]){
                                        setProductAmount(value);
                                        setAmountValidated(true);
                                      }
                                      else{
                                        setAmountValidated(false);                             
                                      }
                                    }
                                    catch(e){
                                      setAmountValidated(false);
                                    }
                                    
                                  })}/>
                                  
                                <InputGroup.Prepend>
                                  <Button variant="dark" id="addToCartBtn" onClick={(event => {
                                    amountValidated ? addToCartHandler(storeProduct["name"]) : alert("Please enter number greater than 0 and smaller than " + storeProduct["amount"]);
                                    })}>
                                      Add To Cart
                                  </Button>
                                </InputGroup.Prepend>
                              </InputGroup>
                          </div>
                          : null
                        }
                      </td>
                  </tr>
                ))
              }
          </tbody>
        </Table>
      </div>
      <Button style={{marginTop: "1%"}} variant="dark" id="back-btn" as={Link} to="/stores" >Back</Button>
    </div>
  );
}

// TODO - add back button


export default StoreProducts;