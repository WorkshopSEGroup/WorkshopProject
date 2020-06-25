import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import * as theService from '../../../services/communication';
import {Container, Table, Form, Button, ProgressBar} from 'react-bootstrap'
import * as BackOption from '../GeneralActions/Back'
import { confirmAlert } from 'react-confirm-alert'; 
import 'react-confirm-alert/src/react-confirm-alert.css'; // Import css

class PurchaseProducts extends React.Component{
  constructor(props){
    super(props);

    this.state={
      purchase_ls: {},
      total_price: 0,
      purchases: [], // purchases = [{store_name, basket_price, products=[{product_name, product_price, amount}]}]
      details_progress: 0,
      delivery_details_filled: false,
      lock_purchase: false,
      name: "",
      address: "",
      city: "",
      country: "",
      zip: "",
      card_number: "",
      month: "",
      year: "",
      holder: "",
      ccv: "",
      id: ""
    }

    this.handleConfirm = this.handleConfirm.bind(this);
    this.isDeliveryFilled = this.isDeliveryFilled.bind(this);
    this.isPaymentFilled = this.isPaymentFilled.bind(this);
  }

  handleConfirm = async ()  => {
    this.setState({lock_purchase: true})
    var payment_details = {'card_number': this.state.card_number, 'month': this.state.month, 'year': this.state.year, 'holder': this.state.holder, 'ccv': this.state.ccv, 'id': this.state.id}
    var delivery_details = {'name': this.state.name, 'address': this.state.address, 'city': this.state.city, 'country': this.state.country, 'zip': this.state.zip}
    const promise = theService.confirmPurchase(delivery_details, payment_details, this.state.purchase_ls)
    promise.then((data) => {
      if(data !== undefined){
        confirmAlert({
          title: data["msg"],
          buttons: [
            {
              label: 'Done',
              onClick: () => {
                this.setState({lock_purchase: false})
                BackOption.BackToHome(this.props)}  
            }
          ]
      });
      }
    })

  }

  componentWillMount = () =>{
    const promise = theService.purchaseCart();
    promise.then((data) => {
      if(data !== null && data !== undefined){
        this.setState({total_price: data["data"]["total_price"], purchases: data["data"]["purchases"], purchase_ls: data["data"]})
      }
    })
  }

  isDeliveryFilled = () =>{
    if(this.state.lock_purchase)
      return false;
    if(this.state.name !== "" && this.state.address !== "" && this.state.city !== "" && 
        this.state.country !== "" && this.state.zip !== ""){
      return true;
    }
    return false;
  }

  isPaymentFilled = () =>{
    if(this.state.card_number !== "" && this.state.month !== "" && this.state.year !== "" && 
        this.state.holder !== "" && this.state.ccv !== "" && this.state.id !== ""){
      return true;
    }
    return false;
  }

  render(){
    return (
      <Container id='container' style={{width: this.props["screenWidth"], height: this.props["screenHeight"]}}>
        <div>
          <h1 style={{marginTop: "2%"}}>Purchase Products</h1>
        </div>

        {
          // purchase = {store_name, basket_price, products=[{product_name, product_price, amount}]}
          this.state.purchases.map(purchase => (
            <div style={{border: "1px solid", borderColor: "#CCCCCC"}}>
              <h2 style={{position: "relative", marginTop:"2%", marginBottom:"2%", right: "40%"}}>Store: {purchase["store_name"]}</h2>
              {
                // purchaseProduct = [{product_name, product_price, amount}]
                // purchase["products"].map(purchaseProduct => (
                  <div style={{marginRight: "2%", marginLeft:"2%"}}>
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
                  </div>
                // ))
              }
              <p style={{position: "relative", right: "-43%"}} >Basket Price: {purchase["basket_price"]}</p>
              </div>
          ))
        }
        <p style={{marginTop:"2%"}}>Total Shopping cart Price: {this.state.total_price}</p>

        {/* here we ask the user for all details needed for payment confirmation (for now address only) */}

        <ProgressBar id='progressbar' now={this.state.details_progress}/>
        {
          !this.state.delivery_details_filled ? 
          <div>
              {/* delivery details: name, address, city, country, zip */}
              <h5 style={{marginTop:"2%"}}>Enter Delivery Details:</h5>

              <Form.Control id="name" value={this.state.name} required type="text" placeholder="Full Name" 
                  onChange={(event => {this.setState({name: event.target.value})})} />

              <Form.Control id="address" value={this.state.address} required type="text" placeholder="Delivery Address" 
                  onChange={(event => {this.setState({address: event.target.value})})} style={{marginTop: "1%"}} />

              <Form.Control id="city" value={this.state.city} required type="text" placeholder="City" 
                  onChange={(event => {this.setState({city: event.target.value})})} style={{marginTop: "1%"}} />

              <Form.Control id="country" value={this.state.country} required type="text" placeholder="Country" 
                  onChange={(event => {this.setState({country: event.target.value})})} style={{marginTop: "1%"}} />

              <Form.Control id="zip" value={this.state.zip} required type="text" placeholder="Zip" 
                  onChange={(event => {this.setState({zip: event.target.value})})} style={{marginTop: "1%"}} />

              <Button id='next-button' variant="dark" style={{marginTop: "1%"}} onClick={event => this.setState({delivery_details_filled: true, details_progress: 50})} disabled={!this.isDeliveryFilled()}>
                Next
              </Button>
          </div>
          : 
          <div>
              {/* payment details: card number, month, year, holder, ccv, id */}
              {/* <Form.Label style={{position: "relative", right: "45%"}}>Payment Details</Form.Label> */}
              <h5 style={{marginTop:"2%"}}>Enter Payment Details:</h5>

              <Form.Control id="card_number" value={this.state.card_number} required type="text" placeholder="Credit Card Number" 
                    onChange={(event => {this.setState({card_number: event.target.value})})} />

              <Form.Control id="month" value={this.state.month} required type="text" placeholder="Month" 
                    onChange={(event => {this.setState({month: event.target.value})})} style={{marginTop: "1%"}} />

              <Form.Control id="year" value={this.state.year} required type="text" placeholder="Year" 
                    onChange={(event => {this.setState({year: event.target.value})})} style={{marginTop: "1%"}} />

              <Form.Control id="holder" value={this.state.holder} required type="text" placeholder="Holder Name" 
                    onChange={(event => {this.setState({holder: event.target.value})})} style={{marginTop: "1%"}} />

              <Form.Control id="ccv" value={this.state.ccv} required type="text" placeholder="CCV" 
                    onChange={(event => {this.setState({ccv: event.target.value})})} style={{marginTop: "1%"}} />

              <Form.Control id="id" value={this.state.id} required type="text" placeholder="ID" 
                    onChange={(event => {this.setState({id: event.target.value})})} style={{marginTop: "1%"}} />

              <Button id='confirm-button' variant="dark" style={{marginTop: "1%"}} onClick={this.handleConfirm} disabled={!this.isPaymentFilled() || this.state.lock_purchase}>
                Confirm Purchase
              </Button>
          </div>
        }
        
        
      </Container>  
    );
  };
}

export default PurchaseProducts;
