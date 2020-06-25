import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Link} from 'react-router-dom'
import * as theService from '../../../services/communication';
import {Button, Accordion, Card, Form, InputGroup, Table, Container} from 'react-bootstrap'
import {IoMdCloseCircle} from 'react-icons/io' 


function ShoppingCart(props){
  useEffect(() => {
    fetchShoppingCart();
  }, []);

  const [shoppingCart, setShoppingCart] = useState([]);

  const [showDeleteProduct, setShowDeleteProduct] = useState(false);
  const [showUpdateAmount, setShowUpdateAmount] = useState(false);
  const [updateAmount, setUpdateAmount] = useState(null);

  const fetchShoppingCart = async () => {
    const promise = theService.displayShoppingCart()
    promise.then((data) => {
      if(data != null){
        if(data["data"].length > 0){
          setShoppingCart(data["data"])
        }
        else
          alert(data["msg"]);
          setShoppingCart(data["data"])

      }
    });
  };


  const updateOrRemoveProductHandler = (action_type, store_name, product_name) => {
    var promise
    if(action_type === 'update')
       promise = theService.updateShoppingCart(action_type, product_name, store_name, updateAmount); // goes to register.js and sends to backend
    else 
       promise = theService.updateShoppingCart(action_type, product_name, store_name, 0); // goes to register.js and sends to backend

    promise.then((data) => {
      if(data['data'] === true){
        alert(data["msg"])
        setUpdateAmount(null)
        setShowDeleteProduct(false)
        setShowUpdateAmount(false)
        fetchShoppingCart()
      }
      else alert(data["msg"])

    });
    //TODO
  }



  return (
      <div style={{width: props["screenWidth"], height: props["screenHeight"]}}>
        <h1 style={{marginTop:"2%"}}>Shopping Cart</h1>
        <Container id='container'>
        
        <Accordion id='accordion' style={{marginTop:"2%"}} >
        { shoppingCart.map(basket => (
            <div>
              <Card id='card'>
                  <Card.Header>
                  <Accordion.Toggle id='accordion-toggle' as={Button} type="radio" variant="link" eventKey="0">
                      Store: {basket["store_name"]}
                  </Accordion.Toggle>
                  </Card.Header>
                  <Accordion.Collapse eventKey="0">
                    <Card.Body>
                
                        <Table id='table' striped bordered hover >
                        <thead>
                            <tr>
                                <th>
                                  {/* for remove product from basket */}
                                </th>
                                <th>Product Name</th>
                                <th>Price</th>
                                <th>Amount</th>
                                <th>
                                  <Form.Check id="add-to-cart-checkbox" type="checkbox" checked={showUpdateAmount} label="Update Amount" onChange={(event) => setShowUpdateAmount(!showUpdateAmount)} />
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                basket["basket"].map(storeProduct => (
                                  <tr>
                                      {
                                        <div style={{position:'inherit',  marginTop:"10%"}}>
                                            <Link class="fa-icon-resize"  title='Remove from basket' onClick={(event => {updateOrRemoveProductHandler("remove", basket["store_name"], storeProduct["product_name"])})}><IoMdCloseCircle /> </Link>
                                        </div>
                                      }
                                      <td>{storeProduct["product_name"]}</td>
                                      <td>{storeProduct["price"]}</td>
                                      <td>{storeProduct["amount"]}</td>
                                      <td>
                                      {
                                        showUpdateAmount ? 
                                        <div>
                                            <InputGroup className="mb-3">
                                              <Form.Control id="product-amount" required type="number" min={0} placeholder="Enter amount" style={{width:"1px"}}
                                                onChange={(event => {setUpdateAmount(event.target.valueAsNumber)
                                                })}/>
                                                
                                              <InputGroup.Prepend>
                                                <Button variant="dark" id="addToCartBtn" onClick={(event => {
                                                  (updateAmount > 0) ? updateOrRemoveProductHandler("update", basket["store_name"], storeProduct["product_name"]) : alert("Please enter number greater than 0.");
                                                  })}>
                                                    update
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
                    </Card.Body>
                  </Accordion.Collapse>
                </Card>
            </div>
          ))
        }
        </Accordion>

        {
          shoppingCart.length > 0 ? 
            <div style={{ marginTop:"2%"}}><Button variant="dark" id="purchaseBtn" as={Link} to="/confirm_purchase" >
              Purchase Shopping Cart
            </Button></div>
            : null
        }

        {/* <div style={{marginTop:"-3.45%", marginRight:"58%"}}><Button variant="dark" id="add_product-button" onClick={event => BackOption.BackToHome(props)}>Back</Button>
        </div> */}
      </Container>
    </div>

      
  );
}

export default ShoppingCart;