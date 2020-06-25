import React from 'react';
import { shallow, mount, render } from '../../../enzyme';
import SearchAndFilterProducts from '../../GuestRole/SearchAndFilterProducts'


it('renders without crashing', () => {
    shallow(<SearchAndFilterProducts />);
  });


describe('systemManagerAPI Test Suite', () => {

  it('should render the form', () => {
      const wrapper = shallow(<SearchAndFilterProducts />);  // shallow renders a single component each time. In other words, Enzyme won’t consider the child elements for the test.
      expect(wrapper.find('#accordion').exists()).toBeDefined();
      expect(wrapper.find('#card').exists()).toBeDefined();
      expect(wrapper.find('#accordion-toggle').exists()).toBeDefined();
      expect(wrapper.find('#form').exists()).toBeDefined();
      expect(wrapper.find('#form-group').exists()).toBeDefined();
      expect(wrapper.find('#form-label').exists()).toBeDefined();
      expect(wrapper.find('#Radios1').exists()).toBeDefined();
      expect(wrapper.find('#Radios2').exists()).toBeDefined();
      expect(wrapper.find('#Radios3').exists()).toBeDefined();
      expect(wrapper.find('#form-control').exists()).toBeDefined();
      expect(wrapper.find('#form-group-2').exists()).toBeDefined();
      expect(wrapper.find('#search-btn').exists()).toBeDefined();
      expect(wrapper.find('#card-2').exists()).toBeDefined();
      expect(wrapper.find('#accordion-toggle-2').exists()).toBeDefined();
      expect(wrapper.find('#form-2').exists()).toBeDefined();
      expect(wrapper.find('#form-2-group-1').exists()).toBeDefined();
      expect(wrapper.find('#form-2-label-1').exists()).toBeDefined();
      expect(wrapper.find('#Radios4').exists()).toBeDefined();
      expect(wrapper.find('#Radios5').exists()).toBeDefined();
      expect(wrapper.find('#form-control-2').exists()).toBeDefined();
      expect(wrapper.find('#form-control-3').exists()).toBeDefined();
      expect(wrapper.find('#form-2-label-2').exists()).toBeDefined();
      expect(wrapper.find('#form-control-4').exists()).toBeDefined();
      expect(wrapper.find('#form-2-group-2').exists()).toBeDefined();
      expect(wrapper.find('#filter-btn').exists()).toBeDefined();
      expect(wrapper.find('#table').exists()).toBeDefined();
      expect(wrapper.find('#add-to-cart-checkbox').exists()).toBeDefined();
      expect(wrapper.find('#product-amount').exists()).toBeDefined();
      expect(wrapper.find('#addToCartBtn').exists()).toBeDefined();
      
  })
});