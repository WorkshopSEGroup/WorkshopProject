import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Container, Button, Accordion, Card, Form, Row} from 'react-bootstrap'
import * as theService from '../../services/communication';
import AddPurchasePolicyForm from './AddPurchasePolicyForm';
import EditPurchasePolicyForm from './EditPurchasePolicyForm';
import AddDiscountPolicyForm from './AddDiscountPolicyForm';
import EditDiscountPolicyForm from './EditDiscountPolicyForm';
import DeletePolicy from './DeletePolicy';
import AddCompositeDiscountPolicyForm from './AddCompositDiscount';

// import Icon from 'react-native-vector-icons/FontAwesome';

function ManageStorePolicies(props) {
  useEffect(() => {
    setStoreName(props.location.store)
  }, []);

  // const [history, setHistory]= useState('');
  const [storeName, setStoreName] = useState('');
  const [purchaseAction, setPurchaseAction] = useState("");
  const [discountAction, setDiscountAction] = useState("");


  
  const addPurchaseHandler = (event) =>{
    setPurchaseAction("addPurchasePolicy")
  };

  const editPurchaseHandler = (event) =>{
    setPurchaseAction("editPurchasePolicy")
  };

  const PurchasesCombinationHandler = (event) =>{
    setPurchaseAction("purchasesCombination")
  };

  const deletePurchasePolicyHandler = (event) =>{
    setPurchaseAction("deletePurchasePolicy")
  };

  const addDiscountHandler = (event) =>{
    setDiscountAction("addDiscountPolicy")
  };

  const editDiscountHandler = (event) =>{
    setDiscountAction("editDiscountPolicy")
  };

  const addComplexDiscountPolicyHandler = (event) =>{
    setDiscountAction("addComplexDiscountPolicy")
  };

  const deleteDiscountPolicyHandler = (event) =>{
    setDiscountAction("deleteDiscountPolicy")
  };


  return (
    <div style={{width: props["screenWidth"], height: props["screenHeight"]}}>
      <div style={{marginTop:"1%"}}>
        <h2> {storeName} - Manage Store Policies </h2>
      </div>

     <Accordion id='accordion'>
        <Card id='card'>
            {/******** Purchase Card *********/}
            <Card.Header>
            <Accordion.Toggle id='accordion-toggle' as={Button} type="radio" variant="link" eventKey="0">
                Purchase Policy
            </Accordion.Toggle>
            </Card.Header>
            <Accordion.Collapse eventKey="0">
            <Card.Body>

            <Container id='container'> 
            <div style={{marginTop:"2%" , marginLeft: "25%", marginRight: "25%", border: "1px solid", borderColor: "#CCCCCC"}}>
                <h3 style={{marginTop:"2%"}}>Select action</h3>
                <Form id='form' style={{marginRight:"5%" , marginLeft: "5%", marginBottom:"2%"}}>
                    <Row><Form.Check inline onClick={addPurchaseHandler} type="radio" label="Add Purchase Policy" name="formHorizontalRadios" id="Radios1"/>
                    </Row>
                    <Row><Form.Check inline onClick={editPurchaseHandler} type="radio" label="Edit Purchase Policy" name="formHorizontalRadios"id="Radios2"/>
                    </Row>
                    <Row><Form.Check inline onClick={PurchasesCombinationHandler} type="radio" label="Edit Policies Combinations" name="formHorizontalRadios"id="Radios3"/>
                    </Row>
                    <Row><Form.Check inline onClick={deletePurchasePolicyHandler} type="radio" label="Delete Policy" name="formHorizontalRadios"id="Radio4"/>
                    </Row>
                </Form>
            </div>
            <div style={{marginTop: "5%"}}>
                { purchaseAction === "addPurchasePolicy" ? <AddPurchasePolicyForm storeName={storeName} history={props.location.props} /> : null }
            </div>
            <div style={{marginTop: "5%"}}>
                { purchaseAction === "editPurchasePolicy" ? <EditPurchasePolicyForm storeName={storeName} history={props.location.props} /> : null }
            </div>
            <div style={{marginTop: "5%"}}>
                { purchaseAction === "purchasesCombination" ? <PurchaseCombinationsForm storeName={storeName} history={props.location.props} /> : null }
            </div>
            <div style={{marginTop: "5%"}}>
                { purchaseAction === "deletePurchasePolicy" ? <DeletePolicy storeName={storeName} policyType='purchase' history={props.location.props} /> : null }
            </div>

            {/* <Button style={{marginTop: "1%"}}  variant="dark" id="add_product-button" onClick={event => BackOption.BackToHome(props.location.props)}>Back</Button> */}
          
            </Container>

            </Card.Body>
            </Accordion.Collapse>
        </Card>
        <Card id='card-2'>
              {/***************** Discount card *******************/}

            <Card.Header>
            <Accordion.Toggle id='accordion-toggle-2' as={Button} variant="link" eventKey="1">
                Discount Policy
            </Accordion.Toggle>
            </Card.Header>
            <Accordion.Collapse eventKey="1">
            <Card.Body>
            <Container id='container-2'> 
            <div style={{marginTop:"2%" , marginLeft: "25%", marginRight: "25%", border: "1px solid", borderColor: "#CCCCCC"}}>
                <h3 style={{marginTop:"2%"}}>Select action</h3>
                <Form id='form-2' style={{marginRight:"5%" , marginLeft: "5%", marginBottom:"2%"}}>
                    <Row><Form.Check onClick={addDiscountHandler} type="radio" label="Add Discount Policy" name="formHorizontalRadios" id="Radios5"/>
                    </Row>
                    <Row><Form.Check inline onClick={addComplexDiscountPolicyHandler} type="radio" label="Add Complex Discount Policy" name="formHorizontalRadios" id="Radios6"/>
                    </Row>
                    <Row><Form.Check inline onClick={editDiscountHandler} type="radio" label="Edit Discount Policy" name="formHorizontalRadios" id="Radios7"/>
                    </Row>
                    <Row><Form.Check inline onClick={deleteDiscountPolicyHandler} type="radio" label="Delete Discount Policy" name="formHorizontalRadios" id="Radios8"/>
                    </Row>
                </Form>
            </div>
            <div style={{marginTop: "5%"}}>
                { discountAction === "addDiscountPolicy" ? <AddDiscountPolicyForm storeName={storeName} history={props.location.props} /> : null }
            </div>
            <div style={{marginTop: "5%"}}>
                { discountAction === "editDiscountPolicy" ? <EditDiscountPolicyForm storeName={storeName} history={props.location.props} /> : null }
            </div>
            <div style={{marginTop: "5%"}}>
                { discountAction === "addComplexDiscountPolicy" ? <AddCompositeDiscountPolicyForm storeName={storeName} history={props.location.props} /> : null }
            </div>
            <div style={{marginTop: "5%"}}>
                { discountAction === "deleteDiscountPolicy" ? <DeletePolicy storeName={storeName} policyType='discount' history={props.location.props} /> : null }
            </div>

          
            </Container>
            </Card.Body>
            </Accordion.Collapse>

      </Card>
      </Accordion>
    </div>
  );
}



export default ManageStorePolicies;

function PurchaseCombinationsForm(props) {
    useEffect(() => {
      // console.log(props.location.state.storeName)
      setStoreName(props.storeName)
      fetchPurchaseCombination(props.storeName)
    }, []);
  
    // const [history, setHistory]= useState('');
    const [storeName, setStoreName] = useState('');
    const [operator, setOperator] = useState('');
  


    const fetchPurchaseCombination = (store_name) => {
        const promise = theService.getPurchasePoliciesOperator(store_name);
        promise.then((data) => {
            setOperator(data["data"])
      });
    };

    const setOperatorHandler = () => {
        const promise = theService.setPurchasePoliciesOperator(storeName, operator);
        promise.then((data) => {
            alert("Purchase Policies combination updated successfully!")
            fetchPurchaseCombination(storeName)
      });
    };
    
    return (
      
        <div style={{marginTop:"2%" , marginLeft: "25%", marginRight: "25%", border: "1px solid", borderColor: "#CCCCCC"}}>
                <h4 style={{marginTop:"2%"}}>Update policies combinations:</h4>
                <Form style={{marginRight:"5%" , marginLeft: "5%", marginBottom:"2%"}}>
                   
                    <label >Select the wanted combination between the policies</label>
                    <Row><Form.Check inline checked={operator === 'xor'} onChange={(event => {setOperator('xor')})} type="radio" label="Activate only one policy" name="formHorizontalRadios" id="xor_operator"/>
                    </Row>
                    <Row><Form.Check inline checked={operator === 'or'} onChange={(event => {setOperator('or')})} type="radio" label="Activate at least one policy" name="formHorizontalRadios"id="or_operator"/>
                    </Row>
                    <Row><Form.Check inline checked={operator === 'and'} onChange={(event => {setOperator('and')})} type="radio" label="Activate all policies" name="formHorizontalRadios"id="and_operator"/>
                    </Row>
                    <Button id='commit-btn' variant='dark' onClick={setOperatorHandler}>Commit Change</Button>
                </Form>
            </div>
    );
}

