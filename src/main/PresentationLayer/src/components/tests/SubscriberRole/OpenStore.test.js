import React from 'react';
import { shallow, mount, render } from '../../../enzyme';
import OpenStore from '../../SubscriberRole/OpenStore'



    it('renders without crashing', () => {
        shallow(<OpenStore />);
    });

describe('OpenStore Test Suite', () => {

    // checking if the form elements exist and renders all elements
    it('should render the form', () => {
        const wrapper = shallow(<OpenStore />);  // shallow renders a single component each time. In other words, Enzyme won’t consider the child elements for the test.

        // expect(wrapper.find('form.open_store').exists()).toBeDefined(); // check that all the elements renders ok
        expect(wrapper.find('#container').exists()).toBeDefined();
        expect(wrapper.find('#form').exists()).toBeDefined();
        expect(wrapper.find('#form-label').exists()).toBeDefined();
        expect(wrapper.find('#open-store-text').exists()).toBeDefined();
        expect(wrapper.find('#open-store-button').exists()).toBeDefined();

        expect(wrapper.find('open-store-text').length).toEqual(0);
    })
});

describe('Text field store name Test Suite', () => {

    //checking if user name field received the expected input
    it('should change the state of the PurchaseHistoryUsersStores component', () => {

        const wrapper = shallow(<OpenStore />);
        //simulate the event onChange, which happens once an input is entered
        wrapper.find('#open-store-text').simulate('change',
            {
                target: {value: 'new store', }
            });
        wrapper.update();
        expect(wrapper.find('#open-store-text').prop('value')).toEqual('new store'); // check that the value of the text field is now set to the input

    })
});

