import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Button, Accordion, Card, Table, Form, Col, Row, InputGroup} from 'react-bootstrap'
import * as theService from '../../services/communication';
import { confirmAlert } from 'react-confirm-alert'; 


function SearchAndFilterProducts(props) {
  useEffect(() => {

  }, []);

  const [storeProducts, setStoreProducts] = useState([]);
  const [productAmount, setProductAmount] = useState(0);
  const [showAddToCart, setShowAddToCart] = useState(false);
  const [amountValidated, setAmountValidated] = useState(true);
  const [input, setInput] = useState("");
  const [searchType, setSearchType] = useState(0);
  const [filterType, setFilterType] = useState(0);
  const [filterCategory, setFilterCategory] = useState("");
  const [filterMinPrice, setFilterMinPrice] = useState(-1);
  const [filterMaxPrice, setFilterMaxPrice] = useState(-1);


  const addToCartHandler = async (store_name, product_name) => {
    // need - store_name, product_name, product_amount
    const promise = theService.addToProductsCart(store_name, product_name , productAmount)
    promise.then((data => {
      if(data != null){
        if(data["msg"] != null){
            if(data['data'] === true){
              confirmAlert({
                title: data["msg"],
                buttons: [
                    {   label: 'ok',
                        onClick: () => { // reset the form in order to add another product
                        setProductAmount(0)
                    }},
                  ]
              });
            }
            else alert(data["msg"]);
        }
      }
    }))
  }

  const showAddToCartHandler = async () => {
      setShowAddToCart(!showAddToCart);
  }

  const SearchProductsHandler = () => {
    const promise = theService.searchProductsBy(searchType, input);
    promise.then((data) => {

      if(data != null){
        if (data["data"] != null && data["data"].length > 0){   // if there are stores to display
          setStoreProducts(data["data"]);
          setSearchType(0);
          setInput("");
        //   alert(data["msg"]);      // no products to display

        }
        else{
        //   alert(data["msg"]);
          setStoreProducts([]);

          alert("There are no results.");      // no products to display
          setSearchType(0);
          setInput("");
        }
      }
  });
};

const FilterProductsHandler = () => {
    if(filterType === 1){
        if(filterMinPrice > filterMaxPrice)
            alert("Error, minimum price can't be greater than maximum");
        else if(filterMinPrice < 0 ||  filterMaxPrice < 0)
            alert("Error, minimum and maximum prices have to be greater than 0.");
        else{
            const promise = theService.filterProductsByRange(storeProducts, filterType, filterMinPrice, filterMaxPrice);
            promise.then((data) => {

                if(data != null){
                if (data["data"] != null && data["data"].length > 0){   // if there are stores to display
                    setStoreProducts(data["data"]);
                    setFilterType(0);
                    setFilterCategory("");
                    setFilterMaxPrice(-1);
                    setFilterMinPrice(-1);
        
                }
                else{
                    setStoreProducts([]);
                    alert("There are no results.");      // no products to display
                    setFilterType(0);
                    setFilterCategory("");
                    setFilterMaxPrice(-1);
                    setFilterMinPrice(-1);
                    
                }
                }
            });
        }
    }
    else if(filterType === 2){
        const promise = theService.filterProductsByCategory(storeProducts, filterType, filterCategory);
        promise.then((data) => {

            if(data != null){
              if (data["data"] != null && data["data"].length > 0){   // if there are stores to display
                setStoreProducts(data["data"]);
              }
              else{
                setStoreProducts([]);
                alert("There are no results.");      // no products to display
              }
            }
        });

    }
    
};

  return (
    <div style={{width: props["screenWidth"], height: props["screenHeight"]}}>
      <div style={{marginTop:"1%"}}>
        <h2>Search and filter Products </h2>
      </div>

     <Accordion id='accordion'>
        <Card id='card'>
            <Card.Header>
            <Accordion.Toggle id='accordion-toggle' as={Button} type="radio" variant="link" eventKey="0">
                Search products
            </Accordion.Toggle>
            </Card.Header>
            <Accordion.Collapse eventKey="0">
            <Card.Body>
                
                {/******** search component *********/}
                <div style={{marginTop:"0.5%" , marginLeft: "10%", marginRight: "10%", border: "1px solid", borderColor: "#CCCCCC"}}>
                    <Form id='form'>
                        <fieldset>
                            <Form.Group id='form-group' as={Row} >
                                <Form.Label id='form-label' as="legend" column sm={2}>
                                    Search products by:
                                </Form.Label>
                                <Form.Check inline onClick={(event => {setSearchType(1)})} type="radio" label="By name" name="formHorizontalRadios" id="Radios1"/>
                                <Form.Check inline onClick={(event => {setSearchType(2)})} type="radio" label="By keyword" name="formHorizontalRadios" id="Radios2"/>
                                <Form.Check inline onClick={(event => {setSearchType(3)})} type="radio" label="By category" name="formHorizontalRadios" id="Radios3"/>
                                <Form.Control id='form-control' disabled={!searchType}  style={{marginRight:"2%" , marginLeft: "2%"}} onChange={(event => {setInput(event.target.value)})} placeholder="Enter relevant text..." />
                            </Form.Group>
                        </fieldset>
                        <Form.Group id='form-group-2' as={Row} style={{marginRight:"1%" , marginLeft: "1%"}}>
                            <Button id='search-btn' type="reset" variant="dark" disabled={!searchType | input === ""} onClick= {(event => {SearchProductsHandler()})} >Search</Button>
                        </Form.Group>
                    </Form>
                </div>

            </Card.Body>
            </Accordion.Collapse>
        </Card>
        <Card id='card-2'>
            <Card.Header>
            <Accordion.Toggle id='accordion-toggle-2' as={Button} variant="link" eventKey="1">
                Filter products
            </Accordion.Toggle>
            </Card.Header>
            <Accordion.Collapse eventKey="1">
            <Card.Body>
                {/******** filter component *********/}
                <div style={{marginTop:"0.5%" , marginLeft: "10%", marginRight: "10%", border: "1px solid", borderColor: "#CCCCCC"}}>
                    <Form id='form-2'>
                        <fieldset>
                        <Form.Group id='form-2-group-1' as={Row} style={{marginTop: "1%", marginRight:"4%" , marginLeft: "0%"}} >
                            <Form.Label id='form-2-label-1' column sm="2">
                                <Form.Check inline onClick={(event => {setFilterType(1)})} type="radio" label="By price range" name="formHorizontalRadios" id="Radios4"/>                                
                            </Form.Label>
                            <Col sm="10">
                                <Form.Control id='form-control-2' type='number' min={0} disabled={(filterType !== 1)} placeholder="Enter min price" onChange={(event =>{
                                                                                                                        setFilterMinPrice(event.target.valueAsNumber); })}/>
                                <Form.Control id='form-control-3' type='number' min={0} disabled={(filterType !== 1)} style={{marginTop: "1%"}} placeholder="Enter max price"  onChange={(event =>{
                                                                                                                        setFilterMaxPrice(event.target.valueAsNumber);})}/>
                            </Col>
                            <Form.Label id='form-2-label-2' column sm="2" >
                                <Form.Check inline onClick={(event => {setFilterType(2)})} type="radio" label="By category" name="formHorizontalRadios" id="Radios5"/>                                
                            </Form.Label>
                            <Col sm="10">
                                <Form.Control id='form-control-4' disabled={(filterType !== 2)} style={{marginTop: "1%"}} placeholder="Enter category" onChange={(event => {setFilterCategory(event.target.value)})}/>
                            </Col>
                                
                        </Form.Group>
                        </fieldset>
                        

                        <Form.Group id='form-2-group-2' as={Row} style={{marginRight:"3%" , marginLeft: "3%"}}>
                            <Button id='filter-btn' type="reset" variant="dark" disabled={(
                                                            !(filterType === 1 && (filterMaxPrice !== -1 && filterMinPrice !== -1)) &&
                                                            !(filterType === 2 && filterCategory !== ""))}onClick= {(event => {FilterProductsHandler()})} >Filter</Button>
                        </Form.Group>
                    </Form>
                </div>
            </Card.Body>
            </Accordion.Collapse>

      </Card>
      </Accordion>
        {/******** diplay products *********/}
      <div style={{marginTop: "3%", marginLeft: "1%", marginRight: "1%"}}>
        <Table id='table' striped bordered hover >
          <thead>
              <tr>
                  <th>Store Name</th>
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
                      <td>{storeProduct["store_name"]}</td>
                      <td>{storeProduct["product_name"]}</td>
                      <td>{storeProduct["price"]}</td>
                      <td>{storeProduct["category"]}</td>
                      <td>{storeProduct["amount"]}</td>
                      <td>
                        {
                          showAddToCart ? 
                          <div>
                              <InputGroup className="mb-3">
                                <Form.Control id="product-amount" required type="number" placeholder="Product amount" style={{width:"1px"}}
                                  onChange={(event => {
                                      let value = event.target.valueAsNumber
                                      if(value > 0 && value <= storeProduct["amount"]){
                                        setProductAmount(value);
                                        setAmountValidated(true);
                                      }
                                      else{
                                        setAmountValidated(false);                             
                                      }
                                    
                                  })}/>
                                  
                                <InputGroup.Prepend>
                                  <Button variant="dark" id="addToCartBtn" onClick={(event => {
                                    amountValidated ? addToCartHandler(storeProduct["store_name"], storeProduct["product_name"]) : alert("Please enter number greater than 0 and smaller than " + storeProduct["amount"]);
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
    </div>
  );
}

// TODO - add back button


export default SearchAndFilterProducts;