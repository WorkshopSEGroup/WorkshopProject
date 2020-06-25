import React from 'react';
import { shallow, mount, render } from '../../../enzyme';
import PurchaseProducts from '../../Actions/ShoppingCartActions/PurchaseProducts'


it('renders without crashing', () => {
    shallow(<PurchaseProducts />);
  });


describe('PurchaseProducts Test Suite', () => {

  // checking if the form elements exist and renders all elements
  it('should render the form', () => {
      const wrapper = shallow(<PurchaseProducts />);  // shallow renders a single component each time. In other words, Enzyme won’t consider the child elements for the test.
      expect(wrapper.find('#container').exists()).toBeDefined();
      expect(wrapper.find('#table').exists()).toBeDefined();
      expect(wrapper.find('#progressbar').exists()).toBeDefined();
      expect(wrapper.find('#name').exists()).toBeDefined();
      expect(wrapper.find('#address').exists()).toBeDefined();
      expect(wrapper.find('#city').exists()).toBeDefined();
      expect(wrapper.find('#country').exists()).toBeDefined();
      expect(wrapper.find('#zip').exists()).toBeDefined();
      expect(wrapper.find('#next-button').exists()).toBeDefined();
      expect(wrapper.find('#card_number').exists()).toBeDefined();
      expect(wrapper.find('#month').exists()).toBeDefined();
      expect(wrapper.find('#year').exists()).toBeDefined();
      expect(wrapper.find('#holder').exists()).toBeDefined();
      expect(wrapper.find('#ccv').exists()).toBeDefined();
      expect(wrapper.find('#id').exists()).toBeDefined();
      expect(wrapper.find('#confirm-button').exists()).toBeDefined();

      expect(wrapper.find('#name').length).toEqual(1);
      expect(wrapper.find('#address').length).toEqual(1);
      expect(wrapper.find('#city').length).toEqual(1);
      expect(wrapper.find('#country').length).toEqual(1);
      expect(wrapper.find('#zip').length).toEqual(1);
      expect(wrapper.find('#card_number').length).toEqual(0);
      expect(wrapper.find('#month').length).toEqual(0);
      expect(wrapper.find('#year').length).toEqual(0);
      expect(wrapper.find('#holder').length).toEqual(0);
      expect(wrapper.find('#ccv').length).toEqual(0);
      expect(wrapper.find('#id').length).toEqual(0);

      const wrapper_updated = skipEnterPaymentDetails(wrapper);
      expect(wrapper_updated.find('#month').length).toEqual(1);
      expect(wrapper_updated.find('#year').length).toEqual(1);
      expect(wrapper_updated.find('#holder').length).toEqual(1);
      expect(wrapper_updated.find('#ccv').length).toEqual(1);
      expect(wrapper_updated.find('#id').length).toEqual(1);
      
  })
});

describe('Name Test Suite', () => {

    it('should change the state of the PurchaseProducts component', () => {

        const wrapper = shallow(<PurchaseProducts />);
        wrapper.find('#name').simulate('change',
            {
                target: { value: 'some name' }
            });
        wrapper.update(); // need to re-render the component to see the changes
        expect(wrapper.find('#name').prop('value')).toEqual('some name'); // check that state was changed
    })
})


describe('Address Test Suite', () => {

    it('should change the state of the PurchaseProducts component', () => {

        const wrapper = shallow(<PurchaseProducts />);
        wrapper.find('#address').simulate('change',
            {
                target: { value: 'address' }
            });
        wrapper.update(); // need to re-render the component to see the changes
        expect(wrapper.find('#address').prop('value')).toEqual('address'); // check that state was changed
    })
})

describe('City Test Suite', () => {

    it('should change the state of the PurchaseProducts component', () => {

        const wrapper = shallow(<PurchaseProducts />);
        wrapper.find('#city').simulate('change',
            {
                target: { value: 'some city' }
            });
        wrapper.update(); // need to re-render the component to see the changes
        expect(wrapper.find('#city').prop('value')).toEqual('some city'); // check that state was changed
    })
})

describe('Country Test Suite', () => {

    it('should change the state of the PurchaseProducts component', () => {

        const wrapper = shallow(<PurchaseProducts />);
        wrapper.find('#country').simulate('change',
            {
                target: { value: 'some country' }
            });
        wrapper.update(); // need to re-render the component to see the changes
        expect(wrapper.find('#country').prop('value')).toEqual('some country'); // check that state was changed
    })
})

describe('Zip Test Suite', () => {

    it('should change the state of the PurchaseProducts component', () => {

        const wrapper = shallow(<PurchaseProducts />);
        wrapper.find('#zip').simulate('change',
            {
                target: { value: 999 }
            });
        wrapper.update(); // need to re-render the component to see the changes
        expect(wrapper.find('#zip').prop('value')).toEqual(999); // check that state was changed
    })
})

describe('Card Number Test Suite', () => {

    it('should change the state of the PurchaseProducts component', () => {

        const wrapper_try = shallow(<PurchaseProducts />);
        const wrapper = skipEnterPaymentDetails(wrapper_try);

        wrapper.find('#card_number').simulate('change',
            {
                target: { value: 999666 }
            });
        wrapper.update(); // need to re-render the component to see the changes
        expect(wrapper.find('#card_number').prop('value')).toEqual(999666); // check that state was changed
    })
});

describe('Month Test Suite', () => {

    it('should change the state of the PurchaseProducts component', () => {

        const wrapper_try = shallow(<PurchaseProducts />);
        const wrapper = skipEnterPaymentDetails(wrapper_try);

        wrapper.find('#month').simulate('change',
            {
                target: { value: 'month' }
            });
        wrapper.update(); // need to re-render the component to see the changes
        expect(wrapper.find('#month').prop('value')).toEqual('month'); // check that state was changed
    })
});

describe('Year Test Suite', () => {

    it('should change the state of the PurchaseProducts component', () => {

        const wrapper_try = shallow(<PurchaseProducts />);
        const wrapper = skipEnterPaymentDetails(wrapper_try);

        wrapper.find('#year').simulate('change',
            {
                target: { value: 2020 }
            });
        wrapper.update(); // need to re-render the component to see the changes
        expect(wrapper.find('#year').prop('value')).toEqual(2020); // check that state was changed
    })
});

describe('Card Holder Test Suite', () => {

    it('should change the state of the PurchaseProducts component', () => {

        const wrapper_try = shallow(<PurchaseProducts />);
        const wrapper = skipEnterPaymentDetails(wrapper_try);

        wrapper.find('#holder').simulate('change',
            {
                target: { value: 'some holder' }
            });
        wrapper.update(); // need to re-render the component to see the changes
        expect(wrapper.find('#holder').prop('value')).toEqual('some holder'); // check that state was changed
    })
});

describe('CCV Test Suite', () => {

    it('should change the state of the PurchaseProducts component', () => {

        const wrapper_try = shallow(<PurchaseProducts />);
        const wrapper = skipEnterPaymentDetails(wrapper_try);

        wrapper.find('#ccv').simulate('change',
            {
                target: { value: 123 }
            });
        wrapper.update(); // need to re-render the component to see the changes
        expect(wrapper.find('#ccv').prop('value')).toEqual(123); // check that state was changed
    })
});

describe('ID Test Suite', () => {

    it('should change the state of the PurchaseProducts component', () => {

        const wrapper_try = shallow(<PurchaseProducts />);
        const wrapper = skipEnterPaymentDetails(wrapper_try);

        wrapper.find('#id').simulate('change',
            {
                target: { value: 123456789 }
            });
        wrapper.update(); // need to re-render the component to see the changes
        expect(wrapper.find('#id').prop('value')).toEqual(123456789); // check that state was changed
    })
});



function skipEnterPaymentDetails(wrapper){
    wrapper.find('#name').simulate('change',
    {
        target: { value: 'some name' }
    });
    wrapper.find('#address').simulate('change',
    {
        target: { value: 'address' }
    });
    wrapper.find('#city').simulate('change',
    {
        target: { value: 'some city' }
    });
    wrapper.find('#country').simulate('change',
    {
        target: { value: 'some country' }
    });
    wrapper.find('#zip').simulate('change',
    {
        target: { value: 999 }
    });
    wrapper.update();

    wrapper.find('#next-button').simulate('click',
        {
            target: { value: '' }
        });
    wrapper.update();
    return wrapper;
};