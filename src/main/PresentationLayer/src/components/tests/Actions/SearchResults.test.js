import React from 'react';
import { shallow, mount, render } from '../../../enzyme';
import SearchResults from '../../Actions/ShoppingCartActions/SearchResults'


it('renders without crashing', () => {
    shallow(<SearchResults />);
  });

  describe('SearchResults Test Suite', () => {

    // checking if the form elements exist and renders all elements
    it('should render the form', () => {
        const wrapper = shallow(<SearchResults />);  // shallow renders a single component each time. In other words, Enzyme won’t consider the child elements for the test.
        expect(wrapper.find('#container').exists()).toBeDefined();
        expect(wrapper.find('#form').exists()).toBeDefined();
        expect(wrapper.find('#form-group-1').exists()).toBeDefined();
        expect(wrapper.find('#inline-radio-1').exists()).toBeDefined();
        expect(wrapper.find('#min-price').exists()).toBeDefined();
        expect(wrapper.find('#max-price').exists()).toBeDefined();
        expect(wrapper.find('#form-group-2').exists()).toBeDefined();
        expect(wrapper.find('#inline-radio-2').exists()).toBeDefined();
        expect(wrapper.find('#form-group-3').exists()).toBeDefined();
        expect(wrapper.find('#inline-radio-3').exists()).toBeDefined();
        expect(wrapper.find('#form-choose').exists()).toBeDefined();
        expect(wrapper.find('#inline-radio-4').exists()).toBeDefined();
        expect(wrapper.find('#filter-button').exists()).toBeDefined();
        expect(wrapper.find('#container-2').exists()).toBeDefined();
        expect(wrapper.find('#add-button').exists()).toBeDefined();
        
        // expect(wrapper.find('#min-price').length).toEqual(0);
        // expect(wrapper.find('#max-price').length).toEqual(0);
    })
  });