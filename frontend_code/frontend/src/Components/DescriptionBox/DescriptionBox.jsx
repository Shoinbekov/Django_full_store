import React from 'react'
import './DescriptionBox.css'

const DescriptionBox = () => {
  return (
    <div className='descriptionbox'>
        <div className="descriptionbox-navigator">
            <div className="descriptionbox-nav-box">
                Description
            </div>
            <div className="descriptionbox-nav-box fade">
                Reviews (122)
            </div>
        </div>
        <div className="descriptionbox-description">
            <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Id commodi quasi sapiente provident dignissimos voluptatem, qui obcaecati itaque reprehenderit perspiciatis adipisci facere debitis consectetur odio quisquam ex doloribus dolor natus.</p>
            <p>
                Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet nisi qui voluptatibus enim quia error harum. Animi qui explicabo porro amet atque accusamus, nostrum praesentium dolorem. Corporis itaque ad reiciendis!
            </p>
        </div>
    </div>
  )
}

export default DescriptionBox