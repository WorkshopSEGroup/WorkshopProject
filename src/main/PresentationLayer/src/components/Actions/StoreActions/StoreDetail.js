import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import {BrowserRouter as Router, Switch, Route, Link} from 'react-router-dom'
import {Container, Button} from 'react-bootstrap'
import * as theService from '../../../services/communication';
import StoreProducts from '../../Actions/StoreActions/StoreProducts';

import {Accordion, Card, Table} from 'react-bootstrap'



function StoreDetail(props) {
  useEffect(() => {
    console.log(props)
    onStoreInfoClickHandler(props.location.state.storeName);
    // setDisplayOption(props.location.state.displayOption)
    // onStoreInfoClickHandler();
  }, []);
  //TODO - need to send a REQUEST to display store's info

  // const [displayOption, setDisplayOption]= useState("");
  const [owners, setOwners]= useState(["empty"]);
  const [managers, setManagers]= useState(["empty"]);
  

  const onStoreInfoClickHandler = (store) => {
    const promise = theService.displayStoresStores(store)
    promise.then((data) => {
      if(data){
        if(data["data"]["name"] !== store){
          alert("different name recieved");
        }
        if(props.location.state.displayOption === "storeInfo"){

          setManagers(data["data"]["managers"]);
          setOwners(data["data"]["owners"]);
        }
      }
    });
  };

  return (
    <div>
      {props.location.state.displayOption === "storeInfo" && <ShowStoreInfo storeName={props.location.state.storeName} managers={managers} owners={owners} />}
      {props.location.state.displayOption === "productsInfo" && <StoreProducts storeName={props.location.state.storeName} onStoreInfoClickHandler={onStoreInfoClickHandler} />}
    </div>
  );
}

function ShowStoreInfo(props){
  return(
    <div>
      <h1>{props.storeName}</h1>
      <div style={{marginTop: "3%", marginLeft: "1%", marginRight: "1%"}}>
        <Accordion id='accordion'>
          <Card id='card'>
            <Card.Header>
              <Accordion.Toggle id='accordion-toggle' as={Button} variant="link" eventKey="0">
                Store Owners
              </Accordion.Toggle>
            </Card.Header>
            <Accordion.Collapse eventKey="0">
              <Card.Body>
                <Table id='table' striped bordered hover >
                  <tbody>
                      {
                          props.owners.map(owner => {
                              return(
                                  <tr>
                                      <td>{owner}</td>
                                  </tr>
                              );
                          })
                      }
                  </tbody>
                </Table>
              </Card.Body>
            </Accordion.Collapse>
          </Card>
          <Card id='card-2'>
            <Card.Header>
              <Accordion.Toggle id='accordion-toggle-2' as={Button} variant="link" eventKey="1">
                Store Managers
              </Accordion.Toggle>
            </Card.Header>
            <Accordion.Collapse eventKey="1">
              <Card.Body>
              <Table id='table-2' striped bordered hover color="black">
                  <tbody>
                      {
                        props.managers == [] || props.managers == null ? <p>No Managers Exsist For The Store Yet!</p> :
                          props.managers.map(manager => {
                              return(
                                  <tr>
                                      <td>{manager}</td>
                                  </tr>
                              );
                          })
                      }
                  </tbody>
                </Table>
              </Card.Body>
            </Accordion.Collapse>
          </Card>
        </Accordion>
      </div>
      <Button style={{marginTop: "1%"}} variant="dark" id="back-btn" as={Link} to="/stores" >Back</Button>

    </div>
  )
}


export default StoreDetail;