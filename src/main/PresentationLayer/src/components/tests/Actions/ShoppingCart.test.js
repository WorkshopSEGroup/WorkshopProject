import * as theService from '../../../services/communication';
import React from 'react';
import { shallow, mount, render } from '../../../enzyme';
import { act } from "react-dom/test-utils";
import ShoppingCart from '../../Actions/ShoppingCartActions/ShoppingCart'


jest.mock('../../../services/communication', () => ({
    displayShoppingCart: jest.fn()
}));
// jest.mock(theService.displayShoppingCart);


    it('renders without crashing', () => {
        shallow(<ShoppingCart />);
    });

describe('ShoppingCart Test Suite', () => {

    // checking if the form elements exist and renders all elements
    it('should render the form', () => {
        const wrapper = shallow(<ShoppingCart />);  // shallow renders a single component each time. In other words, Enzyme won’t consider the child elements for the test.
        expect(wrapper.find('#container').exists()).toBeDefined();
        expect(wrapper.find('#accordion').exists()).toBeDefined();
        expect(wrapper.find('#card').exists()).toBeDefined();
        expect(wrapper.find('#accordion-toggle').exists()).toBeDefined();
        expect(wrapper.find('#table').exists()).toBeDefined();
        expect(wrapper.find('#add-to-cart-checkbox').exists()).toBeDefined();
        expect(wrapper.find('#purchaseBtn').exists()).toBeDefined();

    })
});



//MOCKS
    // it("renders the component correctly", async () => {
    //     const expectedFromBackend = ["first value", "second value"]
    
    //     theService.displayShoppingCart.mockResolvedValue({
    //     data: expectedFromBackend
    //     });

    //     const theShoppingCart = await asyncRender(<ShoppingCart someProperty={"some-property"} />);

    //     expect(theShoppingCart.find('#purchase-button').exists()).toBeDefined();
    //     // console.log(theShoppingCart.find('#purchase-button'));
    //     // expect(theShoppingCart.find('#purchase-button')).toHaveLength(1); // check loading state exists - the state when the component is waiting for backend response

    //     theShoppingCart.update() //after update the response will be updated in the component
    //     const divs = theShoppingCart.find("div");
    //     // console.log(divs);
    //    divs.map((div, index) => {
    //         expect(div.find('#product-button')).toHaveLength(2); // why 4??
    //     expect(div.text()).toEqual(expectedFromBackend[index]); // .text() coverts to text you can see the fisrt and second values inside
    //    });

    // });

  
  async function asyncRender(component) {
      let wrapper;
      // To prepare a component for assertions, wrap the code rendering it and performing updates inside an act() call. This makes your test run closer to how React works in the browser.
      await act(async () => {
        wrapper = mount(component);
      });
    
      return wrapper;
    };
