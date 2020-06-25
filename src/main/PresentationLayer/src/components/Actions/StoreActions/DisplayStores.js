import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import {BrowserRouter as Router, Switch, Route, Link} from 'react-router-dom'
import {Button, Form, Row} from 'react-bootstrap'
import * as theService from '../../../services/communication';


function DisplayStores(props){
  useEffect(() => {
    setCount(count + 1);
    fetchStores();
  }, []);

  const [count, setCount] = useState(1);
  const [selectedStore, setSelectedStore] = useState("");
  const [infoType, setInfoType] = useState("");
  const [stores, setStores] = useState([]); // Declare a new state variable, which we'll call "stores"

  const fetchStores = async () => {
    const promise = theService.displayStores(); // goes to register.js and sends to backend
    promise.then((data) => {
      if(data !== null){
        if (data["data"]["response"].length > 0){   // if there are stores to display
            setStores(data["data"]["response"]);
        }
        else{
          alert(data["data"]["msg"]);      // no stores to display
        }
      }
    });
  };

  return (

      <div style={{width: props["screenWidth"], height: props["screenHeight"]}}>
         <div style={{marginTop:"1%"}}>
             <h2>Store and products info: </h2>
         </div>
         <div style={{marginTop:"1%" , marginLeft: "25%", marginRight: "25%", border: "1px solid", borderColor: "#CCCCCC"}}>
             <Form id="form">
                <Form.Group id='form-group' style={{marginTop:"2%"}} onChange={ event => {setSelectedStore(event.target.value)}}>
                    <Form.Label id="form-label">Please choose a store:</Form.Label>
                    <div style={{marginTop:"1%" , marginLeft: "3%", marginRight: "3%"}}>
                      <Form.Control as="select" id="form-select">
                      <option value={""} >Select Store</option>
                          {stores.map(store => (
                              <option value={store}>{store}</option>
                          ))}
                      </Form.Control>
                    </div>
                </Form.Group>


                <Form id="form-2" style={{marginRight:"5%" , marginLeft: "5%", marginBottom:"2%"}}>
                    <Form.Label id="form-2-label" style={{marginLeft:"1%"}}>
                      Choose Display option:
                    </Form.Label>
                    <Row>
                      <Form.Check id="form-2-check-1" inline onClick={(event => {setInfoType("storeInfo")})} type="radio" label="Store Info" name="formHorizontalRadios" id="Radios1"/>
                    </Row>
                    <Row>
                      <Form.Check id="form-2-check-2" inline onClick={(event => {setInfoType("productsInfo")})} type="radio" label="Store's Products" name="formHorizontalRadios" id="Radios2"/>
                    </Row>
                </Form>

             </Form>
             
        </div>
        <div style={{marginTop:"1%" }}>
          <Link to={{pathname:'/stores/'+selectedStore, 
                                  state:{storeName: selectedStore,
                                         displayOption: infoType}
                                  }}>
              <Button id="display-button" type="reset" variant="dark" disabled={selectedStore === "" | infoType === ""}>Display</Button>
          </Link>
        </div> 

     </div>
  );
}

export default DisplayStores;




          // <h1 key={store.id}>
          //   <Link to={'/stores/${store.id}'}>
          //     <Button variant="dark">{store.name}</Button>
          //   {/* <button type="button" onClick={this.handleRegister}></button> */}
          //   </Link>
          // </h1>