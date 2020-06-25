import React from 'react';
import { shallow, mount, render } from '../../../enzyme';
import PurchaseHistoryUsersStores from '../../SystemManagerRole/PurchaseHistoryUsersStores'



    it('renders without crashing', () => {
        shallow(<PurchaseHistoryUsersStores />);
    });

describe('PurchaseHistoryUsersStores Test Suite', () => {

    // checking if the form elements exist and renders all elements
    it('should render the form', () => {
        const wrapper = shallow(<PurchaseHistoryUsersStores />);  // shallow renders a single component each time. In other words, Enzyme won’t consider the child elements for the test.

        // expect(wrapper.find('form.purchase_history').exists()).toBeDefined(); // check that all the elements renders ok
        // expect(wrapper.find('#purchase-1').exists()).toBeDefined();
        expect(wrapper.find('#purchase-radio-1').exists()).toBeDefined();
        expect(wrapper.find('#purchase-radio-2').exists()).toBeDefined();
        expect(wrapper.find('#purchase-username').exists()).toBeDefined();
        expect(wrapper.find('#purchase-storename').exists()).toBeDefined();
        expect(wrapper.find('#form').exists()).toBeDefined();
        expect(wrapper.find('#purchase-view').exists()).toBeDefined();
        expect(wrapper.find('#back-btn').exists()).toBeDefined();
        expect(wrapper.find('#table').exists()).toBeDefined();
        expect(wrapper.find('#form-2').exists()).toBeDefined();

        //check that test fields are disabled when component renders first time
        expect(wrapper.find('#purchase-username').prop('disabled')).toEqual(true);
        expect(wrapper.find('#purchase-storename').prop('disabled')).toEqual(true);

        expect(wrapper.find('#purchase-username').length).toEqual(1);
        expect(wrapper.find('#purchase-storename').length).toEqual(1);
    })
});

describe('User name Test Suite', () => {

    //checking if user name field received the expected input
    it('should change the state of the PurchaseHistoryUsersStores component', () => {

        const wrapper = shallow(<PurchaseHistoryUsersStores />);
        //simulate the event onChange, which happens once an input is entered
        wrapper.find('#purchase-username').simulate('change',
            {
                target: {value: 'some name', }
            });
        wrapper.update();
        expect(wrapper.find('#purchase-username').prop('value')).toEqual('some name'); // check that the value of the text field is now set to the input

    })
});

describe('Store name Test Suite', () => {

    //checking if store name field received the expected input
    it('should change the state of the PurchaseHistoryUsersStores component', () => {

        const wrapper = shallow(<PurchaseHistoryUsersStores />);
        wrapper.find('#purchase-storename').simulate('change',
            {
                target: {value: 'some store', }
            });
        wrapper.update();
        expect(wrapper.find('#purchase-storename').prop('value')).toEqual('some store'); // check that the value of the text field is now set to the input

    })
});

describe('Radio button 1 (View users’ purchase history) selected Test Suite', () => {

    //checking if radio button was selected upon event
    it('should change the state of the PurchaseHistoryUsersStores component', () => {

        const wrapper = shallow(<PurchaseHistoryUsersStores />);
        wrapper.find('#purchase-radio-1').simulate('change');
        wrapper.update();
        expect(wrapper.find('#purchase-radio-1').prop('checked')).toEqual(true); // check that the value of the text field is now set to the input

    })
});

describe('Radio button 2 (View stores’ purchase history) selected Test Suite', () => {

    //checking if radio button was selected upon event
    it('should change the state of the PurchaseHistoryUsersStores component', () => {

        const wrapper = shallow(<PurchaseHistoryUsersStores />);
        wrapper.find('#purchase-radio-2').simulate('change');
        wrapper.update();
        expect(wrapper.find('#purchase-radio-2').prop('checked')).toEqual(true); // check that the value of the text field is now set to the input

    })
});