import React from 'react';
import { shallow, mount, render } from '../../../enzyme';

import AddProductsForm from '../../OwnerOrManagerRole/AddProductsForm'



it('renders without crashing', () => {
    shallow(<AddProductsForm />);
  });

describe('AddProductsForm Test Suite', () => {

    // checking if the form elements exist.
    it('should render the form', () => {
        const wrapper = shallow(<AddProductsForm />);  // shallow renders a single component each time. In other words, Enzyme won’t consider the child elements for the test.

        expect(wrapper.find('form.add_product').exists()).toBeDefined(); // check that the component renders ok
        expect(wrapper.find('#product-name').exists()).toBeDefined(); 
        expect(wrapper.find('#product-price').exists()).toBeDefined(); 
        expect(wrapper.find('#product-category').exists()).toBeDefined(); 
        expect(wrapper.find('#product-amount').exists()).toBeDefined(); 
        expect(wrapper.find('#open-store-button').exists()).toBeDefined(); 

        expect(wrapper.find('#product-name').length).toEqual(1);   // id syntax - searched for email id
        expect(wrapper.find('#product-price').length).toEqual(1); 
        expect(wrapper.find('#product-category').length).toEqual(1);
        expect(wrapper.find('#product-amount').length).toEqual(1);  
    })
});

describe('Product Name Test Suite', () => {

    it('should change the state of the AddProductsForm component', () => {

        const wrapper = shallow(<AddProductsForm />);
        // simulate an onChange event (when we enter an email input)
        wrapper.find('#product-name').simulate('change',
            {
                target: { value: 'new product' }
            });
        wrapper.update(); // need to re-render the component to see the changes
        expect(wrapper.find('#product-name').prop('value')).toEqual('new product');  // check that state was changed
    })
})

describe('Product Price Test Suite', () => {

    it('should change the state of the AddProductsForm component', () => {

        const wrapper = shallow(<AddProductsForm />);
        wrapper.find('#product-price').simulate('change',
            {
                target: { valueAsNumber: 15 }
            });
        wrapper.update();
        expect(wrapper.find('#product-price').prop('value')).toEqual(15);
    })
});

describe('Product Category Test Suite', () => {

    it('should change the state of the AddProductsForm component', () => {

        const wrapper = shallow(<AddProductsForm />);
        wrapper.find('#product-category').simulate('change',
            {
                target: { value: 'some category' }
            });
        wrapper.update();
        expect(wrapper.find('#product-category').prop('value')).toEqual('some category');
    })
});

describe('Product Amount Test Suite', () => {

    it('should change the state of the AddProductsForm component', () => {

        const wrapper = shallow(<AddProductsForm />);
        wrapper.find('#product-amount').simulate('change',
            {
                target: { valueAsNumber: 3 }
            });
        wrapper.update();
        expect(wrapper.find('#product-amount').prop('value')).toEqual(3);
    })
});

describe('Purchase Type Test Suite', () => {

    it('should change the state of the AddProductsForm component', () => {

        const wrapper = shallow(<AddProductsForm />);
        wrapper.find('#immidiate-purchase').simulate('change',
            {
                target: { value: 3 }
            });
        wrapper.update();
        expect(wrapper.find('#immidiate-purchase').prop('value')).toEqual(3);
    })
});