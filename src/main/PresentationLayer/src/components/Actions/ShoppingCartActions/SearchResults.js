import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Button, Form, Container, Col, Row, Checkbox} from 'react-bootstrap'
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom'
import * as theService from '../../../services/communication';


function SearchResults(props){
    useEffect(() => {
        setSearchOption(props.location.state.searchOption);
        setInput(props.location.state.input);
        setCategories(props.location.state.categories);
        console.log(props);
        fetchProducts();
    }, []);

    // setters/getters for passed argumnets
    const [searchOption, setSearchOption] = useState(0);
    const [input, setInput] = useState("");
    const [categories, setCategories] = useState([]);
    
    const [products, setProducts] = useState([]);

    // setters/getters for 'by price range' option
    const [minValueInput, setMinValueInput] = useState(0);
    const [maxValueInput, setMaxValueInput] = useState(0);

    const [filterOption, setFilterOption] = useState(0);
    const [category, setCategory] = useState("");
    const [filterDetails, setFilterDetails] = useState("");
    // const [selectedProductOption, setSelectedProductOption] = useState("");
    const [selectedProducts, setSelectedProducts] = useState([]);

    const onProductClickHandler = () => {
        alert('Product info Product info')  //TODO, ADD OPTION TO VIEW PRICE, POLICIES
      };

    const onCategorySelect = (event)=>{
        setFilterOption(2);
        setCategory(event.target.value);
    };

    const minInputHandler = (event) =>{
        setFilterOption(1);
        setMinValueInput(event.target.value);
    };
    const maxInputHandler = (event) =>{
        setFilterOption(1);
        setMaxValueInput(event.target.value);
    };

    const selectedProductsHandler = (event) => {
        if(selectedProducts.includes(event.target.value)){
            var index = selectedProducts.indexOf(event.target.value);
            console.log(selectedProducts);
            setSelectedProducts(selectedProducts.splice(index, index+1));
            console.log(selectedProducts);
        }
        else{
            console.log(selectedProducts);
            setSelectedProducts(selectedProducts.concat(event.target.value));
            console.log(selectedProducts);
        }
        console.log(selectedProducts);
    };
  

    // request the corresponding products from the server
    const fetchProducts = async () => {
      const promise = theService.searchProductsBy(searchOption, input); // goes to register.js and sends to backend
      promise.then((data) => {setProducts(data["data"])});
    };

    const fetchCategories = async () =>{
        const promise = theService.getCategories(); // goes to register.js and sends to backend
    promise.then((data) => {setCategories(data["data"])});
    }

    const onFilterClickHandler = (event) => {
        event.preventDefault();
        if(filterOption === 1){
            setFilterDetails({min: minValueInput, max: maxValueInput});    
            const promise = theService.filterProductsBy(products, filterOption, filterDetails); // goes to register.js and sends to backend
            promise.then((data) => {setProducts(data["data"])});     
        }
        else if(filterOption === 2){
            // console.log("got here");
            setFilterDetails(category);
            // console.log([products, filterOption, filterDetails]);
            const promise = theService.filterProductsBy(products, filterOption, filterDetails); // goes to register.js and sends to backend
            promise.then((data) => {setProducts(data["data"])});
        }
    };

    const onAddToCartClickHandler = (event) => {
        const promise = theService.addToProductsCart(selectedProducts); // goes to register.js and sends to backend
        promise.then((data) => {
        alert(data["msg"]);
    });

    };
  


    return (
        // TODO - find a way to send to functions when checking one of the radio boxes!
        <div>
          <h1>Search Results</h1>
        <Container id='container'>
          <Form id='form'>
                <Row>
                    Filter by: 
                    <Col>
                    <Row>
                    <Form.Group id='form-group-1' as={Col}  md="8" controlId="bypricerange">
                        <Form.Check label="price range" type='radio' id={`inline-radio-1`} />
                        <Form.Control id='min-price' required type="text" placeholder="min" className="minvalue" onChange={minInputHandler}/>
                        <Form.Control id='max-price' required type="text" placeholder="max" className="maxvalue" onChange={maxInputHandler}/>
                    </Form.Group>
                    </Row>
                    </Col>

                    <Col>
                    <Row>
                    <Form.Group id='form-group-2'>
                        <Form.Check label="product rate" type='radio' id={`inline-radio-2`} />
                    </Form.Group>
                    </Row>
                    </Col>

                    <Col>
                    <Row>
                    <Form.Group id='form-group-3'>
                        <Form.Check inline label="product category" type='radio' id={`inline-radio-3`} />

                        <Form.Group controlId="formGridState">
                        <Form.Control id='form-choose' as="select" value="Choose..." onClick={fetchCategories} onChange={onCategorySelect}>
                            <option>Choose...</option>
                            {categories.map(category => (
                                <option>{category}</option>
                        ))}
                        </Form.Control>
                        </Form.Group> 

                    </Form.Group>
                    </Row>
                    </Col>

                    <Col>
                    <Row>
                    <Form.Group>
                        <Form.Check inline label="store rate" type='radio' id={`inline-radio-4`} />
                    </Form.Group>
                    </Row>
                    </Col>

                    <Col>
                        <Button id='filter-button' variant="dark" onClick={onFilterClickHandler}>Filter</Button>
                    </Col>
                
                </Row>
            </Form>
            </Container>

            <Container id='container-2'>
            {products.map(product => (
            <h1>
                <Row>
                    <Col />
                    <Col>
                        <Row>
                            <Button variant="dark" onClick={onProductClickHandler}>{product}</Button>
                            <Form.Check label="select" value={product} 
                            onChange={selectedProductsHandler} type='checkbox' id={`inline-radio-1`} />
                        </Row>
                    </Col>
                    <Col />
                </Row>
            </h1>
          ))}

          

            <Button id='add-button' variant="dark" block onClick={onAddToCartClickHandler}>Add to Cart</Button>
            </Container>

</div>
    );
  }


export default SearchResults;

