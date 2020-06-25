import React from 'react';
import { shallow, mount, render } from '../../../enzyme';
import StoreProducts from '../../Actions/StoreActions/StoreProducts'

// const detailsProps = {
//     state:{storeName: "BBB",
//         displayOption: 0}
// }

it('renders without crashing', () => {
    shallow(<StoreProducts />);
});

describe('DisplayStores Test Suite', () => {

// checking if the form elements exist and renders all elements
    it('should render the form', () => {
        const wrapper = shallow(<StoreProducts />);  // shallow renders a single component each time. In other words, Enzyme won’t consider the child elements for the test.
        expect(wrapper.find('#table').exists()).toBeDefined();
        expect(wrapper.find('#add-to-cart-checkbox').exists()).toBeDefined();
        expect(wrapper.find('#product-amount').exists()).toBeDefined();
        expect(wrapper.find('#addToCartBtn').exists()).toBeDefined();
        expect(wrapper.find('#back-btn').exists()).toBeDefined();
        
    })
});

describe('Name Test Suite', () => {

    it('should change the state of the PurchaseProducts component', () => {

        const wrapper = shallow(<StoreProducts />);
        wrapper.find('#add-to-cart-checkbox').simulate('change',
            {
                target: { value: '' }
            });
        wrapper.update(); // need to re-render the component to see the changes

        // wrapper.find('#product-amount').simulate('change',
        //     {
        //         target: { value: 10 }
        //     });

        // expect(wrapper.find('#product-amount').prop('value')).toEqual(10); // check that state was changed
    })
});